"use client";

import { useState } from "react";
import Navbar from "@/components/Navbar";

interface Law {
  id: string;
  numero: string;
  year: number;
  fecha: string;
  epigrafe: string;
  summary?: string;
}

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Law[]>([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    year: "",
    type: "",
  });

  const handleSearch = async () => {
    setLoading(true);
    try {
      // TODO: Replace with actual API call
      const response = await fetch(
        `/api/search?query=${encodeURIComponent(query)}&year=${filters.year}&type=${filters.type}`
      );
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Search error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Navbar />

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-24 pb-12">
        {/* Search Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white sm:text-5xl">
            <span className="gradient-text">Buscar Leyes</span>
          </h1>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
            Encuentra legislación colombiana usando búsqueda semántica
          </p>
        </div>

        {/* Search Box */}
        <div className="glass rounded-2xl p-6 mb-8">
          <div className="flex flex-col gap-4 md:flex-row">
            <div className="flex-1">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                placeholder="Buscar por número, tema, o contenido..."
                className="w-full rounded-lg border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={loading}
              className="rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 px-6 py-3 font-medium text-white transition-all hover:shadow-lg hover:shadow-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Buscando...
                </span>
              ) : (
                "🔍 Buscar"
              )}
            </button>
          </div>

          {/* Filters */}
          <div className="mt-4 flex flex-wrap gap-4">
            <select
              value={filters.year}
              onChange={(e) => setFilters({ ...filters, year: e.target.value })}
              className="rounded-lg border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-2 text-gray-900 dark:text-white focus:border-blue-500 focus:outline-none"
            >
              <option value="">Todos los años</option>
              {Array.from({ length: 30 }, (_, i) => 2026 - i).map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>

            <select
              value={filters.type}
              onChange={(e) => setFilters({ ...filters, type: e.target.value })}
              className="rounded-lg border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-2 text-gray-900 dark:text-white focus:border-blue-500 focus:outline-none"
            >
              <option value="">Todos los tipos</option>
              <option value="ley">Ley</option>
              <option value="decreto">Decreto</option>
              <option value="resolucion">Resolución</option>
              <option value="sentencia">Sentencia</option>
            </select>
          </div>
        </div>

        {/* Results */}
        {results.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Resultados ({results.length})
            </h2>
            <div className="grid gap-4">
              {results.map((law) => (
                <div
                  key={law.id}
                  className="glass rounded-xl p-6 transition-all hover:shadow-xl hover:scale-[1.02]"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                        Ley {law.numero} de {law.year}
                      </h3>
                      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                        {law.fecha}
                      </p>
                      <p className="mt-3 text-gray-700 dark:text-gray-300">
                        {law.epigrafe}
                      </p>
                      {law.summary && (
                        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400 italic">
                          {law.summary}
                        </p>
                      )}
                    </div>
                    <button className="ml-4 rounded-lg bg-blue-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-600">
                      Ver detalles →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No results */}
        {!loading && results.length === 0 && query && (
          <div className="glass rounded-xl p-12 text-center">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              No se encontraron resultados
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Intenta con otros términos de búsqueda o ajusta los filtros
            </p>
          </div>
        )}

        {/* Initial state */}
        {!loading && results.length === 0 && !query && (
          <div className="glass rounded-xl p-12 text-center">
            <div className="text-6xl mb-4">📚</div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              Comienza tu búsqueda
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Ingresa un término, número de ley, o tema para buscar
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
