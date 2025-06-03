import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { supabase } from "./utils/supabaseClient";
import Auth from "./components/Auth";
import Sidebar from "./components/Sidebar";
import JournalHistory from "./pages/JournalHistory";
import NewJournal from "./pages/NewJournal";
import Reflections from "./pages/Reflections";
import "./App.css";

export default function App() {
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

  if (!user) return <Auth />;

  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <div className="main-content">
          <header className="app-header">
            <div className="flex justify-between items-center">
              <h1 className="text-2xl font-bold">Welcome to Voice Journal AI</h1>
              <div className="flex items-center gap-4">
                <span className="text-sm text-muted">{user.email}</span>
                <button
                  onClick={async () => {
                    await supabase.auth.signOut();
                    setUser(null);
                  }}
                  className="sign-out-btn"
                >
                  Sign Out
                </button>
              </div>
            </div>
          </header>
          <main className="content-area">
            <Routes>
              <Route path="/" element={<NewJournal />} />
              <Route path="/journal-history" element={<JournalHistory />} />
              <Route path="/new-journal" element={<NewJournal />} />
              <Route path="/reflections" element={<Reflections />} />
            </Routes>
          </main>
          <footer className="app-footer">
            © 2025 Voice Journal AI. All rights reserved.
          </footer>
        </div>
      </div>
    </Router>
  );
}