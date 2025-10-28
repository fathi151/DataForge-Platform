import React from 'react';
import { CheckCircle, AlertCircle, XCircle } from 'lucide-react';

const ServiceStatus = ({ name, status, port, uptime }) => {
  const statusConfig = {
    running: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-500/10' },
    warning: { icon: AlertCircle, color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
    stopped: { icon: XCircle, color: 'text-red-400', bg: 'bg-red-500/10' }
  };

  const config = statusConfig[status] || statusConfig.stopped;
  const Icon = config.icon;

  return (
    <div className="bg-slate-800 rounded-lg p-4 border border-slate-700 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className={`p-2 rounded-lg ${config.bg}`}>
          <Icon size={20} className={config.color} />
        </div>
        <div>
          <p className="text-white font-medium">{name}</p>
          <p className="text-xs text-slate-400">Port: {port}</p>
        </div>
      </div>
      <div className="text-right">
        <p className={`text-sm font-medium ${config.color}`}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </p>
        {uptime && <p className="text-xs text-slate-400">{uptime}</p>}
      </div>
    </div>
  );
};

export default ServiceStatus;
