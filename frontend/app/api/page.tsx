import Navbar from "@/components/Navbar";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ApiPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Navbar />

      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 pt-24 pb-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white sm:text-5xl">
            <span className="gradient-text">API Docs</span>
          </h1>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
            Documentación y herramientas para integrar con la base legal
            colombiana.
          </p>
        </div>

        <div className="glass rounded-2xl p-8 space-y-6">
          <div>
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
              Base URL
            </h2>
            <p
              data-testid="api-base-url"
              className="mt-2 rounded-lg bg-gray-900/90 px-4 py-3 font-mono text-sm text-white"
            >
              {apiBaseUrl}
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <a
              data-testid="swagger-link"
              href={`${apiBaseUrl}/docs`}
              target="_blank"
              rel="noreferrer"
              className="flex items-center justify-between rounded-xl border border-blue-200/60 bg-white/70 px-5 py-4 text-gray-900 shadow-sm transition hover:border-blue-400 hover:shadow-md"
            >
              <span className="font-semibold">Abrir Swagger UI</span>
              <span className="text-sm text-blue-600">/docs</span>
            </a>
            <a
              data-testid="redoc-link"
              href={`${apiBaseUrl}/redoc`}
              target="_blank"
              rel="noreferrer"
              className="flex items-center justify-between rounded-xl border border-purple-200/60 bg-white/70 px-5 py-4 text-gray-900 shadow-sm transition hover:border-purple-400 hover:shadow-md"
            >
              <span className="font-semibold">Abrir ReDoc</span>
              <span className="text-sm text-purple-600">/redoc</span>
            </a>
          </div>

          <div className="rounded-xl border border-white/40 bg-white/50 p-5">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Endpoints clave
            </h3>
            <ul className="mt-3 space-y-2 text-sm text-gray-700 dark:text-gray-300">
              <li>
                <span className="font-mono">GET /search</span> — Búsqueda de
                leyes
              </li>
              <li>
                <span className="font-mono">GET /laws/:id</span> — Detalle de ley
              </li>
              <li>
                <span className="font-mono">GET /stats</span> — Estadísticas del
                sistema
              </li>
              <li>
                <span className="font-mono">POST /scrape</span> — Ejecutar scraping
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
