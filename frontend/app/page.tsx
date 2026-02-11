import Link from "next/link";
import Image from "next/image";
import Navbar from "@/components/Navbar";
import FeatureCard from "@/components/FeatureCard";
import StatsCard from "@/components/StatsCard";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-24 pb-20">
        {/* Animated background gradient blobs */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 -left-4 h-72 w-72 animate-pulse rounded-full bg-purple-300 opacity-20 blur-3xl dark:bg-purple-900" />
          <div className="absolute top-20 right-4 h-72 w-72 animate-pulse rounded-full bg-blue-300 opacity-20 blur-3xl dark:bg-blue-900" style={{ animationDelay: "1s" }} />
          <div className="absolute -bottom-8 left-20 h-72 w-72 animate-pulse rounded-full bg-cyan-300 opacity-20 blur-3xl dark:bg-cyan-900" style={{ animationDelay: "2s" }} />
        </div>

        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left side - Text content */}
            <div className="text-center lg:text-left">
              <h1 className="text-5xl font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-6xl md:text-7xl">
                <span className="block">Base de Datos</span>
                <span className="block gradient-text">Legal Colombiana</span>
              </h1>
              <p className="mt-6 max-w-2xl text-lg text-gray-600 dark:text-gray-300 sm:text-xl lg:mx-0 mx-auto">
                Consulta, busca y analiza leyes colombianas con inteligencia
                artificial. Accede a información legal actualizada de forma
                rápida y eficiente.
              </p>
              <div className="mt-10 flex flex-col items-center lg:items-start justify-center lg:justify-start gap-4 sm:flex-row">
                <Link
                  href="/search"
                  className="group relative inline-flex items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-blue-500 to-purple-600 px-8 py-4 text-lg font-medium text-white shadow-lg transition-all hover:shadow-2xl hover:shadow-blue-500/50 hover:scale-105"
                >
                  <span className="relative">🔍 Buscar Leyes</span>
                </Link>
                <Link
                  href="/scraper"
                  className="group inline-flex items-center justify-center rounded-full glass px-8 py-4 text-lg font-medium text-gray-900 dark:text-white transition-all hover:shadow-xl"
                >
                  <span className="relative">⚙️ Iniciar Scraper</span>
                </Link>
              </div>
            </div>

            {/* Right side - Image */}
            <div className="relative lg:block hidden">
              <div className="relative aspect-square rounded-3xl overflow-hidden shadow-2xl">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 z-10" />
                <Image
                  src="https://images.unsplash.com/photo-1589829545856-d10d557cf95f?q=80&w=1200&auto=format&fit=crop"
                  alt="Colombian Legal System - Justice and Law"
                  fill
                  className="object-cover"
                  priority
                  sizes="(max-width: 768px) 100vw, 50vw"
                />
              </div>
              {/* Decorative elements */}
              <div className="absolute -bottom-6 -right-6 h-72 w-72 rounded-full bg-gradient-to-br from-blue-400 to-purple-600 opacity-20 blur-3xl -z-10" />
              <div className="absolute -top-6 -left-6 h-72 w-72 rounded-full bg-gradient-to-br from-cyan-400 to-blue-600 opacity-20 blur-3xl -z-10" />
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <StatsCard value="10,000+" label="Leyes Indexadas" icon="📚" trend="up" />
            <StatsCard value="99.9%" label="Precisión AI" icon="🤖" trend="up" />
            <StatsCard value="<2s" label="Tiempo de Búsqueda" icon="⚡" trend="neutral" />
            <StatsCard value="24/7" label="Disponibilidad" icon="🌐" trend="neutral" />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Características Principales
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600 dark:text-gray-300">
              Todo lo que necesitas para trabajar con legislación colombiana
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <FeatureCard
              icon="🔍"
              title="Búsqueda Inteligente"
              description="Encuentra leyes específicas usando búsqueda semántica potenciada por IA"
              gradient="from-blue-500 to-cyan-500"
            />
            <FeatureCard
              icon="🤖"
              title="Análisis con IA"
              description="Resúmenes automáticos y análisis de contenido legal con inteligencia artificial"
              gradient="from-purple-500 to-pink-500"
            />
            <FeatureCard
              icon="⚙️"
              title="Scraping Automático"
              description="Actualización automática desde fuentes oficiales como SUIN-JURISCOL"
              gradient="from-orange-500 to-red-500"
            />
            <FeatureCard
              icon="📊"
              title="Visualización de Datos"
              description="Gráficos y estadísticas sobre tendencias legislativas"
              gradient="from-green-500 to-emerald-500"
            />
            <FeatureCard
              icon="🔐"
              title="API RESTful"
              description="Integra fácilmente con tus aplicaciones usando nuestra API moderna"
              gradient="from-indigo-500 to-blue-500"
            />
            <FeatureCard
              icon="⚡"
              title="Ultra Rápido"
              description="Respuestas en menos de 2 segundos gracias a nuestra infraestructura optimizada"
              gradient="from-yellow-500 to-orange-500"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="glass rounded-3xl p-12 text-center relative overflow-hidden">
            {/* Background gradient */}
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10" />

            <div className="relative">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl">
                ¿Listo para empezar?
              </h2>
              <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600 dark:text-gray-300">
                Accede a toda la legislación colombiana en un solo lugar
              </p>
              <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Link
                  href="/search"
                  className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-blue-500 to-purple-600 px-8 py-4 text-lg font-medium text-white shadow-lg transition-all hover:shadow-2xl hover:shadow-blue-500/50 hover:scale-105"
                >
                  Explorar Base de Datos →
                </Link>
                <Link
                  href="/api"
                  className="inline-flex items-center justify-center rounded-full border-2 border-gray-300 dark:border-gray-600 px-8 py-4 text-lg font-medium text-gray-900 dark:text-white transition-all hover:border-blue-500 hover:text-blue-500"
                >
                  Ver Documentación API
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-800 py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center text-gray-600 dark:text-gray-400">
            <p>
              &copy; 2026 Colombian Legal Database. Powered by AI & Open Source.
            </p>
            <p className="mt-2 text-sm">
              Datos obtenidos de{" "}
              <a
                href="http://www.suin-juriscol.gov.co"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-500"
              >
                SUIN-JURISCOL
              </a>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
