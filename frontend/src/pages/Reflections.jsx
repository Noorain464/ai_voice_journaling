import React, { useEffect, useState } from "react";
import ReflectionDashboard from "../components/ReflectionDashboard";
import { supabase } from "../utils/supabaseClient";

export default function Reflections() {
  const [summary, setSummary] = useState("");
  const [emotionalTrends, setEmotionalTrends] = useState({});
  const [insights, setInsights] = useState([]);
  const [reflectionImageUrl, setReflectionImageUrl] = useState(null);

  useEffect(() => {
    const fetchReflectionData = async () => {
      const { data, error } = await supabase
        .from("conversation_summaries")
        .select("summary, emotions")
        .order("date", { ascending: false })
        .limit(7);

      if (error) {
        console.error("Error fetching reflection data:", error);
      } else {
        const summaries = data.map((entry) => entry.summary).join("\n");
        const emotions = data.flatMap((entry) => entry.emotions);
        const emotionalTrends = emotions.reduce((acc, emotion) => {
          acc[emotion] = (acc[emotion] || 0) + 1;
          return acc;
        }, {});

        setSummary(summaries);
        setEmotionalTrends(emotionalTrends);
        setInsights([
          "You tend to feel anxious mid-week.",
          "Outdoor activities improve your mood.",
        ]);
      }
    };

    fetchReflectionData();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Reflections</h1>
      <ReflectionDashboard
        summary={summary}
        emotionalTrends={emotionalTrends}
        insights={insights}
        reflectionImageUrl={reflectionImageUrl}
      />
    </div>
  );
}