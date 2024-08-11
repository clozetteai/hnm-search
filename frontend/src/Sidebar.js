import React from 'react';
import { MessageSquare } from 'lucide-react';

const Sidebar = ({ chatSessions, onSelectSession, activeSession }) => {
  return (
    <div className="w-64 bg-gray-800 text-white h-screen overflow-y-auto">
      <div className="p-4">
        <h2 className="text-xl font-bold mb-4">Chat Sessions</h2>
        {chatSessions.map((session) => (
          <div
            key={session.id}
            className={`flex items-center p-2 rounded cursor-pointer ${
              activeSession === session.id ? 'bg-blue-600' : 'hover:bg-gray-700'
            }`}
            onClick={() => onSelectSession(session.id)}
          >
            <MessageSquare size={18} className="mr-2" />
            <span className="truncate">{session.title}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
