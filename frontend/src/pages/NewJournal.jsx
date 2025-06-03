import React, { useState, useEffect } from "react";
import Recorder from "../components/Recorder";
import ChatWindow from "../components/ChatWindow";
import MoodWheel from "../components/MoodWheel";
import { supabase } from "../utils/supabaseClient";

export default function NewJournal() {
  const [messages, setMessages] = useState([]);
  const [emotionCounts, setEmotionCounts] = useState({});
  const [user, setUser] = useState(null);

  useEffect(() => {
    const getUser = async () => {
      const { data } = await supabase.auth.getUser();
      setUser(data.user);
    };
    getUser();

    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => {
      listener?.subscription.unsubscribe();
    };
  }, []);

  const handleNewExchange = (userText, aiReply, emotions) => {
    setMessages((prev) => [
      ...prev,
      { role: "user", content: userText },
      { role: "assistant", content: aiReply },
    ]);
    setEmotionCounts((prev) => {
      const updated = { ...prev };
      emotions.forEach((emotion) => {
        updated[emotion] = (updated[emotion] || 0) + 1;
      });
      return updated;
    });
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">New Journal</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-1 space-y-6">
          <div className="card">
            <MoodWheel emotionCounts={emotionCounts} />
          </div>
          <div className="card flex justify-center">
            <Recorder user={user} onExchange={handleNewExchange} />
          </div>
        </div>

        {/* Right Column */}
        <div className="lg:col-span-2 card h-full">
          <ChatWindow messages={messages} />
        </div>
      </div>
    </div>
  );
}