import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, CheckCircle, AlertCircle, Clock } from 'lucide-react';

const Pipelines = () => {
  const [pipelines, setPipelines] = useState([]);

  useEffect(() => {
    const fetchPipelinesData = async () => {
      try {
        // Fetch pipeline status from API
        const pipelinesResponse = await fetch('http://localhost:8000/api/pipelines/status');
        const pipelinesData = await pipelinesResponse.json();

        setPipelines(pipelinesData);
      } catch (error) {
        console.error('Error fetching pipelines data:', error);
        // Fallback to mock data if API fails
        const mockPipelines = [
          {
            id: 1,
            name: 'ETL Pipeline',
            description: 'Main ETL pipeline for data ingestion',
            status: 'running',
            progress: 65,
            lastRun: '2024-01-06 02:00:00',
            nextRun: '2024-01-07 02:00:00',
            duration: '45 minutes',
            tasks: [
              { name: 'Extract', status: 'completed' },
              { name: 'Transform', status: 'running' },
              { name: 'Load', status: 'pending' }
            ]
          },
          {
            id: 2,
            name: 'Maintenance Pipeline',
            description: 'Database maintenance and optimization',
            status: 'completed',
            progress: 100,
            lastRun: '2024-01-06 03:00:00',
            nextRun: '2024-01-13 03:00:00',
            duration: '30 minutes',
            tasks: [
              { name: 'Vacuum', status: 'completed' },
              { name: 'Quality Check', status: 'completed' },
              { name: 'Report', status: 'completed' }
            ]
          }
        ];
        setPipelines(mockPipelines);
      }
    };

    fetchPipelinesData();
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running':
        return <Clock size={20} className="text-blue-400 animate-spin" />;
      case 'completed':
        return <CheckCircle size={20} className="text-green-400" />;
      case 'failed':
        return <AlertCircle size={20} className="text-red-400" />;
      default:
        return <Clock size={20} className="text-slate-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'bg-blue-500/10 text-blue-400';
      case 'completed':
        return 'bg-green-500/10 text-green-400';
      case 'failed':
        return 'bg-red-500/10 text-red-400';
      default:
        return 'bg-slate-500/10 text-slate-400';
    }
  };

  const getTaskStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500/20 text-green-400';
      case 'running':
        return 'bg-blue-500/20 text-blue-400';
      case 'failed':
        return 'bg-red-500/20 text-red-400';
      case 'pending':
        return 'bg-slate-500/20 text-slate-400';
      default:
        return 'bg-slate-500/20 text-slate-400';
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-white">Pipelines</h2>
        <p className="text-slate-400 mt-1">Monitor and manage ETL pipelines</p>
      </div>

      {/* Pipelines List */}
      <div className="space-y-4">
        {pipelines.map((pipeline) => (
          <div
            key={pipeline.id}
            className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden hover:border-slate-600 transition-colors"
          >
            {/* Pipeline Header */}
            <div className="p-6 border-b border-slate-700">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    {getStatusIcon(pipeline.status)}
                    <div>
                      <h3 className="text-lg font-semibold text-white">{pipeline.name}</h3>
                      <p className="text-sm text-slate-400">{pipeline.description}</p>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(pipeline.status)}`}>
                    {pipeline.status.charAt(0).toUpperCase() + pipeline.status.slice(1)}
                  </span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-400">Progress</span>
                  <span className="text-sm font-medium text-white">{pipeline.progress}%</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all"
                    style={{ width: `${pipeline.progress}%` }}
                  ></div>
                </div>
              </div>

              {/* Pipeline Info */}
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-slate-400">Last Run</p>
                  <p className="text-white font-medium">{pipeline.lastRun}</p>
                </div>
                <div>
                  <p className="text-slate-400">Next Run</p>
                  <p className="text-white font-medium">{pipeline.nextRun}</p>
                </div>
                <div>
                  <p className="text-slate-400">Duration</p>
                  <p className="text-white font-medium">{pipeline.duration}</p>
                </div>
              </div>
            </div>

            {/* Tasks */}
            <div className="px-6 py-4 bg-slate-700/30">
              <p className="text-sm font-medium text-slate-300 mb-3">Tasks</p>
              <div className="space-y-2">
                {pipeline.tasks.map((task, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm text-slate-300">{task.name}</span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${getTaskStatusColor(task.status)}`}>
                      {task.status.charAt(0).toUpperCase() + task.status.slice(1)}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="px-6 py-4 bg-slate-700/10 flex items-center justify-end space-x-2">
              <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-300 hover:text-white">
                <Play size={18} />
              </button>
              <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-300 hover:text-white">
                <Pause size={18} />
              </button>
              <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-300 hover:text-white">
                <RotateCcw size={18} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Pipelines;
