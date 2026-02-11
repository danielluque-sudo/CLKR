interface FeatureCardProps {
  icon: string;
  title: string;
  description: string;
  gradient: string;
}

export default function FeatureCard({
  icon,
  title,
  description,
  gradient,
}: FeatureCardProps) {
  return (
    <div className="group relative overflow-hidden rounded-2xl glass p-6 transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/20 hover:scale-105">
      {/* Gradient background on hover */}
      <div
        className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-0 transition-opacity duration-300 group-hover:opacity-10`}
      />

      {/* Content */}
      <div className="relative">
        <div className="mb-4 text-4xl">{icon}</div>
        <h3 className="mb-2 text-xl font-bold text-gray-900 dark:text-white">
          {title}
        </h3>
        <p className="text-gray-600 dark:text-gray-400">{description}</p>
      </div>

      {/* Decorative corner */}
      <div className={`absolute -right-4 -top-4 h-24 w-24 rounded-full bg-gradient-to-br ${gradient} opacity-10 blur-2xl transition-opacity group-hover:opacity-30`} />
    </div>
  );
}
