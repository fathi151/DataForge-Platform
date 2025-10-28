import React, { useState, useEffect } from 'react';
import ServiceStatus from '../components/ServiceStatus';
import StatCard from '../components/StatCard';
import { Server, Cpu, HardDrive, Zap } from 'lucide-react';

const Services = () => {
  const [services, setServices] = useState([]);
  const [systemStats, setSystemStats] = useState({
    cpuUsage: 45,
    memoryUsage: 62,
    diskUsage: 38,
    networkLatency: 12
  });

  useEffect(() => {
    const fetchServicesData = async () => {
      try {
        // Fetch services status
        const servicesResponse = await fetch('http://localhost:8000/api/services/status');
        const servicesData = await servicesResponse.json();

        // Fetch system stats
        const statsResponse = await fetch('http://localhost:8000/api/services/system-stats');
        const statsData = await statsResponse.json();

        setServices(servicesData);
        setSystemStats(statsData);
      } catch (error) {
        console.error('Error fetching services data:', error);
        // Fallback to mock data
        const mockServices = [
          {
            name: 'PostgreSQL',
            status: 'running',
            port: 5432,
            uptime: '7 days 3 hours'
          },
          {
            name: 'Apache Airflow',
            status: 'running',
            port: 8080,
            uptime: '7 days 2 hours'
          },
          {
            name: 'Grafana',
            status: 'running',
            port: 3000,
            uptime: '7 days 1 hour'
          },
          {
            name: 'Jupyter',
            status: 'running',
            port: 8888,
            uptime: '6 days 23 hours'
          },
          {
            name: 'MinIO',
            status: 'running',
            port: 9001,
            uptime: '7 days'
          },
          {
            name: 'Redis',
            status: 'running',
            port: 6379,
            uptime: '7 days 4 hours'
          },
          {
            name: 'Adminer',
            status: 'running',
            port: 8081,
            uptime: '7 days 2 hours'
          }
        ];
        setServices(mockServices);
      }
    };

    fetchServicesData();
  }, []);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-white">Services</h2>
        <p className="text-slate-400 mt-1">Monitor all platform services and system resources</p>
      </div>

      {/* System Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="CPU Usage"
          value={`${systemStats.cpuUsage}%`}
          icon={Cpu}
          color="blue"
        />
        <StatCard
          title="Memory Usage"
          value={`${systemStats.memoryUsage}%`}
          icon={Zap}
          color="purple"
        />
        <StatCard
          title="Disk Usage"
          value={`${systemStats.diskUsage}%`}
          icon={HardDrive}
          color="orange"
        />
        <StatCard
          title="Network Latency"
          value={`${systemStats.networkLatency}ms`}
          icon={Server}
          color="green"
        />
      </div>

      {/* Services Grid */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-white">Running Services</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {services.map((service, index) => (
            <ServiceStatus
              key={index}
              name={service.name}
              status={service.status}
              port={service.port}
              uptime={service.uptime}
            />
          ))}
        </div>
      </div>

      {/* Service Details */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">Service Details</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Service</th>
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Port</th>
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Status</th>
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Uptime</th>
                <th className="text-left py-3 px-4 text-slate-300 font-medium">URL</th>
              </tr>
            </thead>
            <tbody>
              {services.map((service, index) => (
                <tr key={index} className="border-b border-slate-700 hover:bg-slate-700/50 transition-colors">
                  <td className="py-3 px-4 text-white">{service.name}</td>
                  <td className="py-3 px-4 text-slate-300">{service.port}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-green-500/10 text-green-400 rounded text-xs font-medium">
                      Running
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-300">{service.uptime}</td>
                  <td className="py-3 px-4">
                    <a
                      href={`http://localhost:${service.port}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:text-blue-300 transition-colors"
                    >
                      localhost:{service.port}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Links */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">Quick Links</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { name: 'Airflow', url: 'http://localhost:8080', color: 'from-blue-500 to-blue-600' },
            { name: 'Grafana', url: 'http://localhost:3000', color: 'from-orange-500 to-orange-600' },
            { name: 'Jupyter', url: 'http://localhost:8888', color: 'from-purple-500 to-purple-600' },
            { name: 'MinIO', url: 'http://localhost:9001', color: 'from-red-500 to-red-600' },
            { name: 'Adminer', url: 'http://localhost:8081', color: 'from-green-500 to-green-600' },
            { name: 'PostgreSQL', url: 'localhost:5432', color: 'from-indigo-500 to-indigo-600' }
          ].map((link, index) => (
            <a
              key={index}
              href={link.url.startsWith('http') ? link.url : '#'}
              target="_blank"
              rel="noopener noreferrer"
              className={`bg-gradient-to-br ${link.color} p-4 rounded-lg text-white font-medium text-center hover:shadow-lg transition-shadow`}
            >
              {link.name}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Services;
