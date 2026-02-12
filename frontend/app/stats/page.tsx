"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import { api } from "@/lib/api";

type StatsResponse = Record<string, string | number | null>;

const toLabel = (key: string) =>
  key
    .replace(/_/g, " ")
    .replace(/\b\w/g, (match) => match.toUpperCase());

export default function StatsPage() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const loadStats = async () => {
      try {
        const data = await api.getStats();
        if (!isMounted) return;
        setStats(data as StatsResponse);
        setError(null);
      } catch (err) {
        if (!isMounted) return;
        const message = err instanceof Error ? err.message : "Error desconocido";
        setError(message);
        setStats(null);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };

    loadStats();

    return () => {
      isMounted = false;
    };
  }, []);

  const entries = stats ? Object.entries(stats) : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Navbar />

      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pt-24 pb-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white sm:text-5xl">
            <span className="gradient-text">Estadísticas</span>
          </h1>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
            Métricas en tiempo real sobre la base legal.
          </p>
        </div>

        <div className="glass rounded-2xl p-8">
          {isLoading ? (
            <div
              data-testid="stats-loading"
              className="text-center text-gray-600 dark:text-gray-300"
            >
              Cargando estadísticas...
            </div>
          ) : null}

          {!isLoading && error ? (
            <div
              data-testid="stats-error"
              className="rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-red-700"
            >
              {error}
            </div>
          ) : null}

          {!isLoading && !error ? (
            <div
              data-testid="stats-grid"
              className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3"
            >
              {entries.length === 0 ? (
                <div className="col-span-full text-center text-gray-600 dark:text-gray-300">
                  No hay estadísticas disponibles.
                </div>
              ) : (
                entries.map(([key, value]) => (
                  <div
                    key={key}
                    className="rounded-2xl border border-white/40 bg-white/60 p-6 shadow-sm"
                  >
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {toLabel(key)}
                    </p>
                    <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
                      {value ?? "—"}
                    </p>
                  </div>
                ))
              )}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
