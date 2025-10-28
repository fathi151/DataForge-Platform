import React, { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import ChartCard from '../components/ChartCard';
import StatCard from '../components/StatCard';
import { AlertCircle, CheckCircle, TrendingUp } from 'lucide-react';

const DataQuality = () => {
  const [qualityData, setQualityData] = useState({
    overallScore: 98.5,
    validRecords: 125000,
    invalidRecords: 430,
    qualityTrend: [],
    tableQuality: [],
    issues: []
  });

  useEffect(() => {
    const fetchQualityData = async () => {
      try {
        // Fetch data quality metrics
        const qualityResponse = await fetch('http://localhost:8000/api/data-quality/metrics');
        const qualityData = await qualityResponse.json();

        // Quality trend with real dates (last 6 days)
        const today = new Date();
        const trend = [];
        for (let i = 5; i >= 0; i--) {
          const date = new Date(today);
          date.setDate(date.getDate() - i);
          trend.push({
            date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
            score: 95 + (Math.random() * 5) // Simulated trend
          });
        }
        // Set today's score to actual quality score
        trend[trend.length - 1].score = qualityData.overallScore;

        // Table quality from API
        const tableQuality = qualityData.tableQuality.map(table => ({
          table: table.table_name,
          quality: table.total_records > 0 ? (table.valid_records / table.total_records * 100) : 0,
          records: table.total_records
        }));

        // Issues (mock - would need real issue detection)
        const mockIssues = [
          { id: 1, table: 'orders', type: 'Missing Values', severity: 'low', count: 12 },
          { id: 2, table: 'customers', type: 'Duplicate Records', severity: 'medium', count: 5 },
          { id: 3, table: 'products', type: 'Invalid Format', severity: 'high', count: 3 }
        ];

        setQualityData({
          overallScore: qualityData.overallScore,
          validRecords: qualityData.validRecords,
          invalidRecords: qualityData.invalidRecords,
          qualityTrend: trend,
          tableQuality: tableQuality,
          issues: mockIssues
        });
      } catch (error) {
        console.error('Error fetching quality data:', error);
      }
    };

    fetchQualityData();
  }, []);

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'text-red-400 bg-red-500/10';
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/10';
      case 'low':
        return 'text-blue-400 bg-blue-500/10';
      default:
        return 'text-slate-400 bg-slate-500/10';
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-white">Data Quality</h2>
        <p className="text-slate-400 mt-1">Monitor and manage data quality metrics</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard
          title="Overall Quality Score"
          value={`${qualityData.overallScore}%`}
          icon={CheckCircle}
          color="green"
        />
        <StatCard
          title="Valid Records"
          value={qualityData.validRecords.toLocaleString()}
          icon={TrendingUp}
          color="blue"
        />
        <StatCard
          title="Invalid Records"
          value={qualityData.invalidRecords.toLocaleString()}
          icon={AlertCircle}
          color="red"
        />
      </div>

      {/* Quality Trend */}
      <ChartCard title="Quality Score Trend" subtitle="Last 6 days">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={qualityData.qualityTrend}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="date" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" domain={[90, 100]} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px'
              }}
            />
            <Line
              type="monotone"
              dataKey="score"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ fill: '#10b981' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Table Quality */}
      <ChartCard title="Table Quality Scores" subtitle="By table">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={qualityData.tableQuality}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="table" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px'
              }}
            />
            <Legend />
            <Bar dataKey="quality" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Issues */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">Data Quality Issues</h3>
        <div className="space-y-3">
          {qualityData.issues.map((issue) => (
            <div
              key={issue.id}
              className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
            >
              <div className="flex-1">
                <p className="text-white font-medium">{issue.type}</p>
                <p className="text-sm text-slate-400">Table: {issue.table}</p>
              </div>
              <div className="flex items-center space-x-4">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getSeverityColor(issue.severity)}`}>
                  {issue.severity.charAt(0).toUpperCase() + issue.severity.slice(1)}
                </span>
                <span className="text-white font-medium">{issue.count} records</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DataQuality;
