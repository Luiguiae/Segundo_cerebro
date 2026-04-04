import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function SeccionLista({ titulo, items, campoNombre, onCreate, onToggle, onDelete }) {
  const [nuevoNombre, setNuevoNombre] = useState("");

  const crear = async () => {
    if (!nuevoNombre.trim()) return;
    await onCreate(nuevoNombre.trim());
    setNuevoNombre("");
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-5 flex flex-col gap-4">
      <h2 className="font-semibold text-gray-800">{titulo}</h2>

      <ul className="flex flex-col gap-2">
        {items.map((item) => (
          <li
            key={item.id}
            className="flex items-center justify-between gap-2 text-sm"
          >
            <span className={item.activa ? "text-gray-800" : "text-gray-400 line-through"}>
              {item[campoNombre]}
            </span>
            <div className="flex gap-2">
              <button
                onClick={() => onToggle(item)}
                className="text-xs text-indigo-600 hover:underline"
              >
                {item.activa ? "Desactivar" : "Activar"}
              </button>
              <button
                onClick={() => onDelete(item.id)}
                className="text-xs text-red-500 hover:underline"
              >
                Eliminar
              </button>
            </div>
          </li>
        ))}
      </ul>

      <div className="flex gap-2 pt-1">
        <input
          type="text"
          value={nuevoNombre}
          onChange={(e) => setNuevoNombre(e.target.value)}
          placeholder={`Nueva ${titulo.toLowerCase().slice(0, -1)}…`}
          className="flex-1 border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
          onKeyDown={(e) => e.key === "Enter" && crear()}
        />
        <button
          onClick={crear}
          disabled={!nuevoNombre.trim()}
          className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-sm font-medium rounded-md px-3 py-1.5 transition-colors"
        >
          Agregar
        </button>
      </div>
    </div>
  );
}

export default function Configuracion() {
  const [tematicas, setTematicas] = useState([]);
  const [fuentes,   setFuentes]   = useState([]);
  const [error,     setError]     = useState("");

  const cargar = async () => {
    try {
      const [rt, rf] = await Promise.all([
        fetch(`${API}/tematicas/`).then((r) => r.json()),
        fetch(`${API}/fuentes/`).then((r) => r.json()),
      ]);
      setTematicas(rt);
      setFuentes(rf);
    } catch {
      setError("No se pudo conectar con el servidor.");
    }
  };

  useEffect(() => { cargar(); }, []);

  // Temáticas
  const crearTematica = async (nombre) => {
    const res = await fetch(`${API}/tematicas/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre }),
    });
    if (res.status === 409) { setError("Ya existe una temática con ese nombre."); return; }
    setError("");
    await cargar();
  };

  const toggleTematica = async (t) => {
    await fetch(`${API}/tematicas/${t.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ activa: !t.activa }),
    });
    await cargar();
  };

  const eliminarTematica = async (id) => {
    await fetch(`${API}/tematicas/${id}`, { method: "DELETE" });
    await cargar();
  };

  // Fuentes
  const crearFuente = async (url) => {
    const res = await fetch(`${API}/fuentes/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    if (res.status === 409) { setError("Ya existe una fuente con esa URL."); return; }
    setError("");
    await cargar();
  };

  const toggleFuente = async (f) => {
    await fetch(`${API}/fuentes/${f.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ activa: !f.activa }),
    });
    await cargar();
  };

  const eliminarFuente = async (id) => {
    await fetch(`${API}/fuentes/${id}`, { method: "DELETE" });
    await cargar();
  };

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-xl font-bold text-gray-900">Configuración</h1>

      {error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-4 py-2">
          {error}
        </p>
      )}

      <SeccionLista
        titulo="Temáticas"
        items={tematicas}
        campoNombre="nombre"
        onCreate={crearTematica}
        onToggle={toggleTematica}
        onDelete={eliminarTematica}
      />

      <SeccionLista
        titulo="Fuentes"
        items={fuentes}
        campoNombre="url"
        onCreate={crearFuente}
        onToggle={toggleFuente}
        onDelete={eliminarFuente}
      />
    </div>
  );
}
