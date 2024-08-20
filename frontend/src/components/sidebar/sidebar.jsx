import React, { useState, useEffect } from 'react';
import { Search, PlusCircle, ChevronLeft, ChevronRight, LogOut } from 'lucide-react';
import { APPLOGO } from '../../assets';

const Sidebar = ({ chatSessions, onSelectSession, activeSession, isSettingsPage = false }) => {
  const [isExpanded, setIsExpanded] = useState(() => {
    if (isSettingsPage) {
      return false; // Always start collapsed on settings page
    }
    const saved = localStorage.getItem('sidebarExpanded');
    return saved !== null ? JSON.parse(saved) : true;
  });
  
  
  const onLogout = () => {
    // implement logout
  }

  useEffect(() => {
    if (!isSettingsPage) {
      localStorage.setItem('sidebarExpanded', JSON.stringify(isExpanded));
    }
  }, [isExpanded, isSettingsPage]);

  const toggleSidebar = () => {
    setIsExpanded(!isExpanded);
  };
  const groupSessions = (sessions) => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const sevenDaysAgo = new Date(today);
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    const groups = {
      today: [],
      yesterday: [],
      previous7Days: [],
      previous30Days: [],
      older: []
    };

    sessions.forEach(session => {
      const sessionDate = new Date(session.updated_at);
      if (sessionDate >= today) {
        groups.today.push(session);
      } else if (sessionDate >= yesterday) {
        groups.yesterday.push(session);
      } else if (sessionDate >= sevenDaysAgo) {
        groups.previous7Days.push(session);
      } else if (sessionDate >= thirtyDaysAgo) {
        groups.previous30Days.push(session);
      } else {
        groups.older.push(session);
      }
    });

    // Sort sessions within each group
    Object.keys(groups).forEach(key => {
      groups[key].sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
    });

    return groups;
  };

  const sortedGroupedSessions = groupSessions(chatSessions);

  const renderSessionGroup = (title, sessions) => {
    if (sessions.length === 0) return null;
    return (
      <div key={title} className="mt-4">
        <h3 className="px-3 py-2 text-sm font-semibold text-gray-500">{title}</h3>
        {sessions.map((session) => (
          <button
            key={session.session_id}
            className={`flex w-full flex-col gap-y-2 rounded-lg px-3 py-2 text-left transition-colors duration-200 ${
              activeSession === session.session_id
                ? 'bg-slate-200 light:bg-slate-800'
                : 'hover:bg-slate-200 light:hover:bg-slate-800'
            } focus:outline-none`}
            onClick={() => onSelectSession(session.session_id)}
          >
            <h1 className="text-sm capitalize text-slate-700 light:text-slate-400">
              {session.title}
            </h1>
            <p className="text-xs text-slate-500 light:text-slate-400">
              {new Date(session.updated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </p>
          </button>
        ))}
      </div>
    );
  };


  return (
    <aside className="flex font-poppins">
      {/* First Column */}
      <div className="flex h-screen w-12 flex-col items-center justify-between border-r border-slate-300 bg-slate-50 py-8 light:border-slate-700 light:bg-slate-900 sm:w-16">
        {/* Top section */}
        <div className="flex flex-col items-center space-y-8">
          {/* Logo */}
          <a href="/" className="mb-1">
            <img src={APPLOGO} className='h-10' alt="" />
          </a>

          {/* New conversation */}
          <a href="/chat" className="rounded-lg p-1.5 text-slate-500 transition-colors duration-200 hover:bg-slate-200 focus:outline-none light:text-slate-400 light:hover:bg-slate-800">
            <PlusCircle className="h-6 w-6" />
          </a>
          {/* User */}
          <a
            href="/"
            className="rounded-lg p-1.5 text-slate-500 transition-colors duration-200 hover:bg-slate-200 focus:outline-none light:text-slate-400 light:hover:bg-slate-800"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              viewBox="0 0 24 24"
              strokeWidth="2"
              stroke="currentColor"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
              <path d="M12 10m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"></path>
              <path
                d="M6.168 18.849a4 4 0 0 1 3.832 -2.849h4a4 4 0 0 1 3.834 2.855"
              ></path>
            </svg>
          </a>
          {/* settings */}
          <a
            href="/settings"
            className="rounded-lg p-1.5 text-slate-500 transition-colors duration-200 hover:bg-slate-200 focus:outline-none light:text-slate-400 light:hover:bg-slate-800"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              viewBox="0 0 24 24"
              strokeWidth="2"
              stroke="currentColor"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path
                d="M19.875 6.27a2.225 2.225 0 0 1 1.125 1.948v7.284c0 .809 -.443 1.555 -1.158 1.948l-6.75 4.27a2.269 2.269 0 0 1 -2.184 0l-6.75 -4.27a2.225 2.225 0 0 1 -1.158 -1.948v-7.285c0 -.809 .443 -1.554 1.158 -1.947l6.75 -3.98a2.33 2.33 0 0 1 2.25 0l6.75 3.98h-.033z"
              ></path>
              <path d="M12 12m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"></path>
            </svg>
          </a>
        </div>

        {/* Bottom section */}
        <div className="flex flex-col items-center space-y-4">
          {/* Toggle sidebar button */}
          {!isSettingsPage && (
            <button
              onClick={toggleSidebar}
              className="rounded-lg p-1.5 text-slate-500 transition-colors duration-200 hover:bg-slate-200 focus:outline-none light:text-slate-400 light:hover:bg-slate-800"
            >
              {isExpanded ? <ChevronLeft className="h-6 w-6" /> : <ChevronRight className="h-6 w-6" />}
            </button>
          )}
          
          {/* Logout button */}
          <button
            onClick={onLogout}
            className="rounded-lg p-1.5 text-slate-500 transition-colors duration-200 hover:bg-slate-200 focus:outline-none light:text-slate-400 light:hover:bg-slate-800"
          >
            <LogOut className="h-6 w-6" />
          </button>
        </div>
      </div>
      {/* Second Column */}
      {isExpanded && !isSettingsPage && (
        <div className="h-screen w-52 overflow-y-auto bg-slate-50 py-8 light:bg-slate-900 sm:w-60">
          <div className="flex items-start">
            <h2 className="inline px-5 text-lg font-medium text-slate-800 light:text-slate-200">
              Chats
            </h2>
            <span className="rounded-full bg-blue-600 px-2 py-1 text-xs text-slate-200">
              {chatSessions.length}
            </span>
          </div>

          <div className="mx-2 mt-8 space-y-4">
            <form>
              <label htmlFor="search-chats" className="sr-only">Search chats</label>
              <div className="relative">
                <input
                  id="search-chats"
                  type="text"
                  className="w-full rounded-lg border border-slate-300 bg-slate-50 p-3 pr-10 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 light:border-slate-700 light:bg-slate-900 light:text-slate-200"
                  placeholder="Search chats"
                  required
                />
                <button
                  type="submit"
                  className="absolute bottom-2 right-2.5 rounded-lg p-2 text-sm text-slate-500 hover:text-blue-700 focus:outline-none sm:text-base"
                >
                  <Search className="h-5 w-5" />
                  <span className="sr-only">Search chats</span>
                </button>
              </div>
            </form>

            {renderSessionGroup('Today', sortedGroupedSessions.today)}
            {renderSessionGroup('Yesterday', sortedGroupedSessions.yesterday)}
            {renderSessionGroup('Previous 7 Days', sortedGroupedSessions.previous7Days)}
            {renderSessionGroup('Previous 30 Days', sortedGroupedSessions.previous30Days)}
            {renderSessionGroup('Older', sortedGroupedSessions.older)}
          </div>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;