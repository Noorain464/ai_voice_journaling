import React, { useEffect, useState } from "react";
import { supabase } from "../utils/supabaseClient";

export default function JournalHistory() {
  const [summaries, setSummaries] = useState([]);

  useEffect(() => {
    const fetchSummaries = async () => {
      const { data, error } = await supabase
        .from("conversation_summaries")
        .select("date, summary")
        .order("date", { ascending: false });

      if (error) {
        console.error("Error fetching summaries:", error);
      } else {
        setSummaries(data);
      }
    };

    fetchSummaries();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Journal History</h1>
      <div className="space-y-4">
        {summaries.map((entry, idx) => (
          <div key={idx} className="card">
            <h3 className="font-semibold text-lg mb-2">
              {new Date(entry.date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </h3>
            <p className="text-gray-600">{entry.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}