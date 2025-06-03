import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const EMOTION_COLOR_MAP = {
  joy: "#7FC6A4",
  anger: "#FFA987",
  sadness: "#5D737E",
  fear: "#1A4B5F",
  neutral: "#E8E8E8",
};

export default function MoodWheel({ emotionCounts }){
  const data = Object.entries(emotionCounts)
    .filter(([_, count]) => count > 0)
    .map(([emotion, count]) => ({
      name: emotion.charAt(0).toUpperCase() + emotion.slice(1),
      value: count,
      color: EMOTION_COLOR_MAP[emotion] || "#D3D3D3",
    }));

  return (
    <div className="w-full h-full flex flex-col items-center p-4 space-y-4">
      <div className="text-center space-y-1">
        <h3 className="text-lg font-semibold text-gray-800">
          Your Emotional Landscape
        </h3>
        <p className="text-sm text-gray-500 max-w-xs mx-auto">
          Visual representation of your journal entries' emotional tone
        </p>
      </div>

      <div className="w-full h-52">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={70}
              paddingAngle={1}
              dataKey="value"
              label={({ name }) => name}
              labelLine={false}
            >
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.color} 
                  stroke="#FFF"
                  strokeWidth={1}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="w-full px-4">
        <div className="grid grid-cols-2 gap-2">
          {data.map((emotion) => (
            <div 
              key={emotion.name} 
              className="flex items-center space-x-2 text-sm"
            >
              <span 
                className="w-3 h-3 rounded-full flex-shrink-0"
                style={{ backgroundColor: emotion.color }}
              />
              <span className="text-gray-600">{emotion.name}</span>
              <span className="font-medium">{emotion.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};