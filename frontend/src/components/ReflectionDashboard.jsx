import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function ReflectionDashboard({ summary, emotionalTrends, insights, reflectionImageUrl }) {
  const trendsData = Object.entries(emotionalTrends).map(([emotion, count]) => ({ 
    emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1), 
    count 
  }));

  return (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Weekly Summary</h3>
        <p className="text-gray-600 whitespace-pre-line">{summary || "No summary available yet."}</p>
      </div>

      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Emotional Trends</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={trendsData}>
              <XAxis dataKey="emotion" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#4F46E5" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Insights</h3>
        <ul className="list-disc list-inside text-gray-600 space-y-1">
          {insights.length > 0 ? (
            insights.map((insight, idx) => (
              <li key={idx}>{insight}</li>
            ))
          ) : (
            <li>No insights available yet.</li>
          )}
        </ul>
      </div>

      {reflectionImageUrl && (
        <div className="card flex justify-center">
          <img 
            src={reflectionImageUrl} 
            alt="Reflection" 
            className="rounded-lg max-h-96 object-contain" 
          />
        </div>
      )}
    </div>
  );
}