import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Database,
  Zap,
  Server,
  BarChart3,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

const Sidebar = ({ isOpen }) => {
  const location = useLocation();

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/data-quality', label: 'Data Quality', icon: Database },
    { path: '/pipelines', label: 'Pipelines', icon: Zap },
    { path: '/services', label: 'Services', icon: Server },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <aside
      className={`${
        isOpen ? 'w-64' : 'w-20'
      } bg-slate-800 border-r border-slate-700 transition-all duration-300 flex flex-col`}
    >
      {/* Logo */}
      <div className="p-4 border-b border-slate-700">
        <div className="flex items-center justify-center h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
          <span className={`font-bold text-white ${!isOpen && 'hidden'}`}>
            DP
          </span>
        </div>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                active
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-300 hover:bg-slate-700'
              }`}
            >
              <Icon size={20} />
              {isOpen && <span className="text-sm font-medium">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-700">
        <div className="text-xs text-slate-400 text-center">
          {isOpen && <p>Data Platform v1.0</p>}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
