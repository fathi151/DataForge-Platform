import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import DataQuality from './pages/DataQuality';
import Pipelines from './pages/Pipelines';
import Services from './pages/Services';
import Analytics from './pages/Analytics';
import './App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    // Apply theme
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <Router>
      <div className="flex h-screen bg-slate-900">
        <Sidebar isOpen={sidebarOpen} />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header 
            onMenuClick={() => setSidebarOpen(!sidebarOpen)}
            onThemeToggle={toggleTheme}
            theme={theme}
          />
          <main className="flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/data-quality" element={<DataQuality />} />
              <Route path="/pipelines" element={<Pipelines />} />
              <Route path="/services" element={<Services />} />
              <Route path="/analytics" element={<Analytics />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
