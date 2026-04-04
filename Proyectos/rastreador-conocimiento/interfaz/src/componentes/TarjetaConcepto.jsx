import { useState } from "react";

const SECCIONES = [
  { clave: "que_es",          etiqueta: "¿Qué es?"                },
  { clave: "por_que_importa", etiqueta: "¿Por qué importa?"       },
  { clave: "como_funciona",   etiqueta: "¿Cómo funciona?"         },
  { clave: "ejemplos",        etiqueta: "Ejemplos concretos"       },
  { clave: "tensiones",       etiqueta: "Tensiones o limitaciones" },
  { clave: "se_conecta_con",  etiqueta: "Se conecta con..."        },
  { clave: "citas",           etiqueta: "Citas o fragmentos clave" },
  { clave: "mis_notas",       etiqueta: "Mis notas"                },
];

export default function TarjetaConcepto({ concepto, onAprobar, onRechazar }) {
  const [expandida, setExpandida] = useState(false);

  const tags = (() => {
    try { return JSON.parse(concepto.tags || "[]"); } catch { return []; }
  })();

  const resumen = concepto.que_es
    ? concepto.que_es.slice(0, 200) + (concepto.que_es.length > 200 ? "…" : "")
    : "Sin descripción.";

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-5 flex flex-col gap-3 shadow-sm">

      {/* Cabecera: título + badge temática + botón expandir */}
      <div className="flex items-start justify-between gap-4">
        <button
          onClick={() => setExpandida((v) => !v)}
          className="flex items-start gap-2 text-left group flex-1 min-w-0"
        >
          <span className="mt-0.5 shrink-0 text-gray-400 group-hover:text-indigo-500 transition-colors">
            {expandida ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            )}
          </span>
          <h2 className="text-base font-semibold text-gray-900 group-hover:text-indigo-700 leading-snug transition-colors">
            {concepto.titulo}
          </h2>
        </button>

        {concepto.tematica_nombre && (
          <span className="shrink-0 text-xs bg-indigo-50 text-indigo-700 rounded-full px-2 py-0.5 font-medium">
            {concepto.tematica_nombre}
          </span>
        )}
      </div>

      {/* Resumen siempre visible */}
      <p className="text-sm text-gray-600 leading-relaxed">
        {expandida ? concepto.que_es || "Sin descripción." : resumen}
      </p>

      {/* Tags */}
      {tags.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {tags.map((tag) => (
            <span key={tag} className="text-xs bg-gray-100 text-gray-500 rounded px-2 py-0.5">
              #{tag}
            </span>
          ))}
        </div>
      )}

      {/* Secciones expandidas */}
      {expandida && (
        <div className="flex flex-col gap-4 pt-2 border-t border-gray-100">
          {SECCIONES.slice(1).map(({ clave, etiqueta }) => {
            const contenido = concepto[clave];
            if (!contenido || contenido === "Sin información disponible.") return null;
            return (
              <div key={clave}>
                <p className="text-xs font-semibold text-indigo-600 uppercase tracking-wide mb-1">
                  {etiqueta}
                </p>
                <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                  {contenido}
                </p>
              </div>
            );
          })}
        </div>
      )}

      {/* Acciones */}
      <div className="flex gap-2 pt-1">
        <button
          onClick={() => onAprobar(concepto.id)}
          className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-md py-2 transition-colors"
        >
          Aprobar
        </button>
        <button
          onClick={() => onRechazar(concepto.id)}
          className="flex-1 bg-white hover:bg-red-50 text-red-600 border border-red-200 text-sm font-medium rounded-md py-2 transition-colors"
        >
          Rechazar
        </button>
      </div>
    </div>
  );
}
