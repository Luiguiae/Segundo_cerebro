import { NavLink, Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Cola from "./vistas/Cola";
import Configuracion from "./vistas/Configuracion";
import Exportacion from "./vistas/Exportacion";

const NAVEGACION = [
  { ruta: "/",              etiqueta: "Cola de revisión" },
  { ruta: "/configuracion", etiqueta: "Configuración"   },
  { ruta: "/exportacion",   etiqueta: "Exportación"     },
];

export default function Aplicacion() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <nav className="bg-white border-b border-gray-200 px-6 py-3 flex gap-6">
          {NAVEGACION.map(({ ruta, etiqueta }) => (
            <NavLink
              key={ruta}
              to={ruta}
              end={ruta === "/"}
              className={({ isActive }) =>
                isActive
                  ? "font-semibold text-indigo-600 border-b-2 border-indigo-600 pb-1"
                  : "text-gray-500 hover:text-gray-800 pb-1"
              }
            >
              {etiqueta}
            </NavLink>
          ))}
        </nav>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/"              element={<Cola />}          />
            <Route path="/configuracion" element={<Configuracion />} />
            <Route path="/exportacion"   element={<Exportacion />}   />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
