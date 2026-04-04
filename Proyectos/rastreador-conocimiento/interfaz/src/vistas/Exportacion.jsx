import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function Exportacion() {
  const [aprobados,   setAprobados]   = useState([]);
  const [seleccion,   setSeleccion]   = useState([]);
  const [cargando,    setCargando]    = useState(false);
  const [exportando,  setExportando]  = useState(false);
  const [error,       setError]       = useState("");

  const cargarAprobados = async () => {
    setCargando(true);
    try {
      // Reutilizamos GET /conceptos filtrando por estado aprobado en el cliente
      // (el endpoint devuelve pendientes; para aprobados usamos el mismo endpoint
      // con el parámetro de estado cuando esté disponible, por ahora llamamos
      // a un endpoint dedicado que agregamos más adelante — usamos stub local)
      const res = await fetch(`${API}/conceptos/aprobados`);
      if (!res.ok) throw new Error();
      setAprobados(await res.json());
    } catch {
      setError("No se pudieron cargar los conceptos aprobados.");
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => { cargarAprobados(); }, []);

  const toggleSeleccion = (id) =>
    setSeleccion((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );

  const seleccionarTodos = () =>
    setSeleccion(
      seleccion.length === aprobados.length ? [] : aprobados.map((c) => c.id)
    );

  const exportar = async () => {
    if (seleccion.length === 0) return;
    setExportando(true);
    setError("");
    try {
      const res = await fetch(`${API}/exportar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ids: seleccion }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Error al exportar.");
      }
      // Descargar el zip
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement("a");
      a.href     = url;
      a.download = "conceptos.zip";
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(e.message);
    } finally {
      setExportando(false);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-xl font-bold text-gray-900">Exportación</h1>

      {error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-4 py-2">
          {error}
        </p>
      )}

      <div className="bg-white border border-gray-200 rounded-lg p-5 flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-gray-700">
            {aprobados.length} concepto{aprobados.length !== 1 ? "s" : ""} aprobado{aprobados.length !== 1 ? "s" : ""}
          </p>
          {aprobados.length > 0 && (
            <button
              onClick={seleccionarTodos}
              className="text-xs text-indigo-600 hover:underline"
            >
              {seleccion.length === aprobados.length ? "Deseleccionar todos" : "Seleccionar todos"}
            </button>
          )}
        </div>

        {cargando ? (
          <p className="text-sm text-gray-500">Cargando…</p>
        ) : aprobados.length === 0 ? (
          <p className="text-sm text-gray-400 text-center py-8">
            No hay conceptos aprobados todavía.
          </p>
        ) : (
          <ul className="flex flex-col gap-2">
            {aprobados.map((c) => (
              <li
                key={c.id}
                onClick={() => toggleSeleccion(c.id)}
                className={`flex items-center gap-3 p-3 rounded-md border cursor-pointer transition-colors ${
                  seleccion.includes(c.id)
                    ? "bg-indigo-50 border-indigo-300"
                    : "bg-white border-gray-200 hover:bg-gray-50"
                }`}
              >
                <input
                  type="checkbox"
                  readOnly
                  checked={seleccion.includes(c.id)}
                  className="accent-indigo-600 w-4 h-4"
                />
                <span className="text-sm text-gray-800">{c.titulo}</span>
              </li>
            ))}
          </ul>
        )}

        <button
          onClick={exportar}
          disabled={seleccion.length === 0 || exportando}
          className="self-start bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-sm font-medium rounded-md px-5 py-2 transition-colors"
        >
          {exportando
            ? "Generando zip…"
            : `Exportar seleccionados (${seleccion.length})`}
        </button>
      </div>
    </div>
  );
}
