import React, { useState, useEffect } from 'react';
import { Search, PlusCircle, ChevronLeft, ChevronRight } from 'lucide-react';

const Sidebar = ({ chatSessions, onSelectSession, activeSession }) => {
  const [isExpanded, setIsExpanded] = useState(() => {
    const saved = localStorage.getItem('sidebarExpanded');
    return saved !== null ? JSON.parse(saved) : true;
  });

  useEffect(() => {
    localStorage.setItem('sidebarExpanded', JSON.stringify(isExpanded));
  }, [isExpanded]);

  const toggleSidebar = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <aside className="flex font-poppins">
      {/* First Column */}
      <div className="flex h-screen w-12 flex-col items-center space-y-8 border-r border-slate-300 bg-slate-50 py-8 light:border-slate-700 light:bg-slate-900 sm:w-16">
        {/* Logo */}
        <a href="/" className="mb-1">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-7 w-7 text-blue-600"
            fill="currentColor"
            strokeWidth="1"
            viewBox="0 0 24 24"
          >
            <path d="M20.553 3.105l-6 3C11.225 7.77 9.274 9.953 8.755 12.6c-.738 3.751 1.992 7.958 2.861 8.321A.985.985 0 0012 21c6.682 0 11-3.532 11-9 0-6.691-.9-8.318-1.293-8.707a1 1 0 00-1.154-.188zm-7.6 15.86a8.594 8.594 0 015.44-8.046 1 1 0 10-.788-1.838 10.363 10.363 0 00-6.393 7.667 6.59 6.59 0 01-.494-3.777c.4-2 1.989-3.706 4.728-5.076l5.03-2.515A29.2 29.2 0 0121 12c0 4.063-3.06 6.67-8.046 6.965zM3.523 5.38A29.2 29.2 0 003 12a6.386 6.386 0 004.366 6.212 1 1 0 11-.732 1.861A8.377 8.377 0 011 12c0-6.691.9-8.318 1.293-8.707a1 1 0 011.154-.188l6 3A1 1 0 018.553 7.9z"></path>
          </svg>
        </a>

        {/* New conversation */}
        <a href="/" className="rounded-lg p-1.5 text-slate-500 transition-colors duration-200 hover:bg-slate-200 focus:outline-none light:text-slate-400 light:hover:bg-slate-800">
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
        {/* Toggle sidebar button */}
        <button
          onClick={toggleSidebar}
          className="mt-auto rounded-lg p-1.5 text-slate-500 transition-colors duration-200 hover:bg-slate-200 focus:outline-none light:text-slate-400 light:hover:bg-slate-800"
        >
          {isExpanded ? <ChevronLeft className="h-6 w-6" /> : <ChevronRight className="h-6 w-6" />}
        </button>
      </div>
      {/* Second Column */}
      {isExpanded && (
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

            {chatSessions.map((session) => (
              <button
                key={session.id}
                className={`flex w-full flex-col gap-y-2 rounded-lg px-3 py-2 text-left transition-colors duration-200 ${activeSession === session.id
                  ? 'bg-slate-200 light:bg-slate-800'
                  : 'hover:bg-slate-200 light:hover:bg-slate-800'
                  } focus:outline-none`}
                onClick={() => onSelectSession(session.id)}
              >
                <h1 className="text-sm capitalize text-slate-700 light:text-slate-400">
                  {session.title}
                </h1>
                <p className="text-xs text-slate-500 light:text-slate-400">
                  {session.date}
                </p>
              </button>
            ))}
          </div>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;