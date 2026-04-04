import { useEffect, useState } from "react";
import TarjetaConcepto from "../componentes/TarjetaConcepto";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function Cola() {
  const [conceptos, setConceptos]     = useState([]);
  const [tematicas, setTematicas]     = useState([]);
  const [seleccion, setSeleccion]     = useState([]);
  const [cargando, setCargando]       = useState(false);
  const [buscando, setBuscando]       = useState(false);
  const [error, setError]             = useState("");
  const [urlManual, setUrlManual]     = useState("");
  const [procesando, setProcesando]   = useState(false);

  const cargarConceptos = async () => {
    setCargando(true);
    try {
      const res = await fetch(`${API}/conceptos`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setConceptos(data);
      setError("");
    } catch (e) {
      if (e instanceof TypeError) {
        // TypeError = fallo de red real (servidor caído, CORS bloqueado)
        setError("No se pudo conectar con el servidor.");
      }
      // Errores HTTP (4xx, 5xx) se loguean pero no muestran el mensaje genérico
    } finally {
      setCargando(false);
    }
  };

  const cargarTematicas = async () => {
    try {
      const res = await fetch(`${API}/tematicas/`);
      const data = await res.json();
      setTematicas(data.filter((t) => t.activa));
    } catch {
      // silencioso — las temáticas son secundarias al cargar
    }
  };

  useEffect(() => {
    cargarConceptos();
    cargarTematicas();
  }, []);

  const toggleTematica = (id) =>
    setSeleccion((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );

  const buscar = async () => {
    if (seleccion.length === 0) return;
    setBuscando(true);
    setError("");
    try {
      const res = await fetch(`${API}/buscar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ids_tematicas: seleccion }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Error al buscar.");
      }
      await cargarConceptos();
    } catch (e) {
      setError(e.message);
    } finally {
      setBuscando(false);
    }
  };

  const procesarEntrada = async () => {
    if (!urlManual.trim()) return;
    setProcesando(true);
    setError("");
    try {
      const res = await fetch(`${API}/procesar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entrada: urlManual.trim() }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Error al procesar.");
      }
      setUrlManual("");
      await cargarConceptos();
    } catch (e) {
      setError(e.message);
    } finally {
      setProcesando(false);
    }
  };

  const aprobar = async (id) => {
    await fetch(`${API}/conceptos/${id}/aprobar`, { method: "PATCH" });
    setConceptos((prev) => prev.filter((c) => c.id !== id));
  };

  const rechazar = async (id) => {
    await fetch(`${API}/conceptos/${id}`, { method: "DELETE" });
    setConceptos((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-xl font-bold text-gray-900">Cola de revisión</h1>

      {/* Búsqueda por temática */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 flex flex-col gap-3">
        <p className="text-sm font-medium text-gray-700">Buscar por temática</p>
        <div className="flex flex-wrap gap-2">
          {tematicas.map((t) => (
            <button
              key={t.id}
              onClick={() => toggleTematica(t.id)}
              className={`text-sm rounded-full px-3 py-1 border transition-colors ${
                seleccion.includes(t.id)
                  ? "bg-indigo-600 text-white border-indigo-600"
                  : "bg-white text-gray-600 border-gray-300 hover:border-indigo-400"
              }`}
            >
              {t.nombre}
            </button>
          ))}
        </div>
        <button
          onClick={buscar}
          disabled={seleccion.length === 0 || buscando}
          className="self-start bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-sm font-medium rounded-md px-4 py-2 transition-colors"
        >
          {buscando ? "Buscando…" : `Buscar (${seleccion.length} seleccionadas)`}
        </button>
      </div>

      {/* Entrada manual */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 flex flex-col gap-3">
        <p className="text-sm font-medium text-gray-700">Procesar URL o texto</p>
        <div className="flex gap-2">
          <input
            type="text"
            value={urlManual}
            onChange={(e) => setUrlManual(e.target.value)}
            placeholder="https://... o pega texto directamente"
            className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            onKeyDown={(e) => e.key === "Enter" && procesarEntrada()}
          />
          <button
            onClick={procesarEntrada}
            disabled={!urlManual.trim() || procesando}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-sm font-medium rounded-md px-4 py-2 transition-colors"
          >
            {procesando ? "Procesando…" : "Procesar"}
          </button>
        </div>
      </div>

      {error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-4 py-2">
          {error}
        </p>
      )}

      {/* Cola de conceptos */}
      {cargando ? (
        <p className="text-sm text-gray-500">Cargando conceptos…</p>
      ) : conceptos.length === 0 ? (
        <p className="text-sm text-gray-400 text-center py-12">
          No hay conceptos pendientes. Lanza una búsqueda para empezar.
        </p>
      ) : (
        <div className="grid gap-4">
          {conceptos.map((c) => (
            <TarjetaConcepto
              key={c.id}
              concepto={c}
              onAprobar={aprobar}
              onRechazar={rechazar}
            />
          ))}
        </div>
      )}
    </div>
  );
}
