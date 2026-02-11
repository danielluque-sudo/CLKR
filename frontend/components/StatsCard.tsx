interface StatsCardProps {
  value: string;
  label: string;
  icon: string;
  trend?: "up" | "down" | "neutral";
}

export default function StatsCard({ value, label, icon, trend = "neutral" }: StatsCardProps) {
  const trendColors = {
    up: "text-green-500",
    down: "text-red-500",
    neutral: "text-gray-500",
  };

  const trendIcons = {
    up: "↗",
    down: "↘",
    neutral: "→",
  };

  return (
    <div className="glass rounded-xl p-6 transition-all duration-300 hover:shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
            {label}
          </p>
          <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
            {value}
          </p>
        </div>
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-purple-600 text-2xl">
          {icon}
        </div>
      </div>
      {trend && (
        <div className={`mt-4 flex items-center text-sm ${trendColors[trend]}`}>
          <span className="mr-1">{trendIcons[trend]}</span>
          <span>Trending {trend}</span>
        </div>
      )}
    </div>
  );
}
