import React from "react";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2 className="text-2xl font-bold mb-8">Voice Journal AI</h2>
      <nav className="flex flex-col space-y-2">
        <NavLink
          to="/new-journal"
          className={({ isActive }) => 
            `nav-link ${isActive ? 'active' : ''}`
          }
        >
          📝 New Journal
        </NavLink>
        <NavLink
          to="/journal-history"
          className={({ isActive }) => 
            `nav-link ${isActive ? 'active' : ''}`
          }
        >
          📜 Journal History
        </NavLink>
        <NavLink
          to="/reflections"
          className={({ isActive }) => 
            `nav-link ${isActive ? 'active' : ''}`
          }
        >
          💭 Reflections
        </NavLink>
      </nav>
    </div>
  );
}