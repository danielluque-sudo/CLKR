"use client";

import { useState } from "react";
import Navbar from "@/components/Navbar";

interface ScraperStatus {
  running: boolean;
  progress: number;
  current_year?: number;
  laws_scraped: number;
  errors: number;
  estimated_time?: string;
}

export default function ScraperPage() {
  const [status, setStatus] = useState<ScraperStatus>({
    running: false,
    progress: 0,
    laws_scraped: 0,
    errors: 0,
  });
  const [config, setConfig] = useState({
    year: new Date().getFullYear(),
    max_laws: 100,
    use_ai: true,
  });

  const startScraper = async () => {
    try {
      const response = await fetch("/api/scrape", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config),
      });
      const data = await response.json();
      setStatus({ ...status, running: true });
      // TODO: Implement WebSocket for real-time updates
    } catch (error) {
      console.error("Scraper error:", error);
    }
  };

  const stopScraper = async () => {
    try {
      await fetch("/api/scrape/stop", { method: "POST" });
      setStatus({ ...status, running: false });
    } catch (error) {
      console.error("Stop error:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Navbar />

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-24 pb-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white sm:text-5xl">
            <span className="gradient-text">Scraper Control</span>
          </h1>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
            Automatiza la recolección de leyes desde SUIN-JURISCOL
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
          {/* Configuration Panel */}
          <div className="glass rounded-2xl p-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              ⚙️ Configuración
            </h2>

            <div className="space-y-4">
              {/* Year */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Año
                </label>
                <input
                  type="number"
                  value={config.year}
                  onChange={(e) =>
                    setConfig({ ...config, year: parseInt(e.target.value) })
                  }
                  min="1900"
                  max={new Date().getFullYear()}
                  className="w-full rounded-lg border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3 text-gray-900 dark:text-white focus:border-blue-500 focus:outline-none"
                  disabled={status.running}
                />
              </div>

              {/* Max Laws */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Máximo de leyes (0 = ilimitado)
                </label>
                <input
                  type="number"
                  value={config.max_laws}
                  onChange={(e) =>
                    setConfig({ ...config, max_laws: parseInt(e.target.value) })
                  }
                  min="0"
                  className="w-full rounded-lg border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3 text-gray-900 dark:text-white focus:border-blue-500 focus:outline-none"
                  disabled={status.running}
                />
              </div>

              {/* Use AI */}
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="use-ai"
                  checked={config.use_ai}
                  onChange={(e) =>
                    setConfig({ ...config, use_ai: e.target.checked })
                  }
                  className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  disabled={status.running}
                />
                <label
                  htmlFor="use-ai"
                  className="ml-3 text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                  🤖 Procesar con IA (resúmenes automáticos)
                </label>
              </div>

              {/* Controls */}
              <div className="pt-4">
                {!status.running ? (
                  <button
                    onClick={startScraper}
                    className="w-full rounded-lg bg-gradient-to-r from-green-500 to-emerald-600 px-6 py-3 font-medium text-white transition-all hover:shadow-lg hover:shadow-green-500/50"
                  >
                    ▶️ Iniciar Scraping
                  </button>
                ) : (
                  <button
                    onClick={stopScraper}
                    className="w-full rounded-lg bg-gradient-to-r from-red-500 to-pink-600 px-6 py-3 font-medium text-white transition-all hover:shadow-lg hover:shadow-red-500/50"
                  >
                    ⏹️ Detener Scraping
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Status Panel */}
          <div className="glass rounded-2xl p-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              📊 Estado
            </h2>

            <div className="space-y-6">
              {/* Status Badge */}
              <div className="flex items-center justify-between">
                <span className="text-gray-700 dark:text-gray-300">Estado:</span>
                <span
                  className={`inline-flex items-center rounded-full px-4 py-1 text-sm font-medium ${
                    status.running
                      ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                      : "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200"
                  }`}
                >
                  {status.running ? "🟢 Activo" : "⚫ Detenido"}
                </span>
              </div>

              {/* Progress Bar */}
              {status.running && (
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-700 dark:text-gray-300">
                      Progreso
                    </span>
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {status.progress}%
                    </span>
                  </div>
                  <div className="h-3 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-300"
                      style={{ width: `${status.progress}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Stats */}
              <div className="grid grid-cols-2 gap-4">
                <div className="rounded-lg bg-blue-50 dark:bg-blue-900/20 p-4">
                  <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                    {status.laws_scraped}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Leyes procesadas
                  </div>
                </div>
                <div className="rounded-lg bg-red-50 dark:bg-red-900/20 p-4">
                  <div className="text-3xl font-bold text-red-600 dark:text-red-400">
                    {status.errors}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Errores
                  </div>
                </div>
              </div>

              {/* Current Year */}
              {status.current_year && (
                <div className="rounded-lg bg-purple-50 dark:bg-purple-900/20 p-4">
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Año actual:
                  </div>
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    {status.current_year}
                  </div>
                </div>
              )}

              {/* Estimated Time */}
              {status.estimated_time && (
                <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span className="mr-2">⏱️</span>
                  <span>Tiempo estimado: {status.estimated_time}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Info Cards */}
        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div className="glass rounded-xl p-6">
            <div className="text-3xl mb-3">🌐</div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
              Fuente Oficial
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Datos obtenidos directamente de SUIN-JURISCOL, la base de datos
              oficial del gobierno colombiano.
            </p>
          </div>

          <div className="glass rounded-xl p-6">
            <div className="text-3xl mb-3">🤖</div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
              Procesamiento IA
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Cada ley es procesada con Claude AI para generar resúmenes y
              análisis automático.
            </p>
          </div>

          <div className="glass rounded-xl p-6">
            <div className="text-3xl mb-3">💾</div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
              Almacenamiento
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Los datos se guardan en Supabase para consultas rápidas y
              eficientes.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
