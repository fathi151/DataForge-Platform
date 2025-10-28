import React from 'react';
import { Menu, Moon, Sun, Bell, User } from 'lucide-react';

const Header = ({ onMenuClick, onThemeToggle, theme }) => {
  return (
    <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <button
          onClick={onMenuClick}
          className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
        >
          <Menu size={20} className="text-slate-300" />
        </button>
        <h1 className="text-xl font-bold text-white">Data Platform Dashboard</h1>
      </div>

      <div className="flex items-center space-x-4">
        {/* Notifications */}
        <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors relative">
          <Bell size={20} className="text-slate-300" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        {/* Theme Toggle */}
        <button
          onClick={onThemeToggle}
          className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
        >
          {theme === 'dark' ? (
            <Sun size={20} className="text-slate-300" />
          ) : (
            <Moon size={20} className="text-slate-300" />
          )}
        </button>

        {/* User Profile */}
        <button className="flex items-center space-x-2 px-3 py-2 hover:bg-slate-700 rounded-lg transition-colors">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <User size={16} className="text-white" />
          </div>
          <span className="text-sm text-slate-300">Admin</span>
        </button>
      </div>
    </header>
  );
};

export default Header;
