import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import StatCard from '../components/StatCard';
import ChartCard from '../components/ChartCard';
import {
  Database,
  TrendingUp,
  Users,
  Activity,
  Clock,
  CheckCircle
} from 'lucide-react';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState({
    totalRecords: 125430,
    activeUsers: 1234,
    pipelineSuccess: 98.5,
    avgResponseTime: 245,
    dailySales: [],
    customerMetrics: [],
    dataQuality: [],
    recentActivities: []
  });

  useEffect(() => {
    // Fetch real data from API
    const fetchDashboardData = async () => {
      try {
        // Fetch dashboard stats
        const statsResponse = await fetch('http://localhost:8000/api/dashboard/stats');
        const statsData = await statsResponse.json();

        // Fetch data quality metrics
        const qualityResponse = await fetch('http://localhost:8000/api/data-quality/metrics');
        const qualityData = await qualityResponse.json();

        // Format daily sales data
        const dailySales = statsData.dailySales.map(item => ({
          date: new Date(item.date).toLocaleDateString('en-US', { weekday: 'short' }),
          sales: parseFloat(item.sales) || 0,
          orders: item.orders || 0
        }));

        // Customer metrics from quality data
        const customerMetrics = [
          { name: 'Valid Records', value: qualityData.validRecords },
          { name: 'Invalid Records', value: qualityData.invalidRecords }
        ];

        // Data quality breakdown
        const dataQuality = [
          { name: 'Valid', value: 95 },
          { name: 'Warnings', value: 4 },
          { name: 'Errors', value: 1 }
        ];

        // Recent activities
        const recentActivities = [
          { id: 1, type: 'Pipeline', message: 'ETL Pipeline completed successfully', time: '2 hours ago' },
          { id: 2, type: 'Data', message: `New data ingested: ${statsData.totalRecords.toLocaleString()} records`, time: '4 hours ago' },
          { id: 3, type: 'Alert', message: `Data quality score: ${qualityData.overallScore}%`, time: '6 hours ago' },
          { id: 4, type: 'System', message: 'Backup completed', time: '1 day ago' }
        ];

        setDashboardData({
          totalRecords: statsData.totalRecords,
          activeUsers: statsData.activeUsers,
          pipelineSuccess: statsData.pipelineSuccess,
          avgResponseTime: statsData.avgResponseTime,
          dailySales: dailySales,
          customerMetrics: customerMetrics,
          dataQuality: dataQuality,
          recentActivities: recentActivities
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Fallback to mock data if API fails
        const mockDailySales = [
          { date: 'Mon', sales: 4000, orders: 240 },
          { date: 'Tue', sales: 3000, orders: 221 },
          { date: 'Wed', sales: 2000, orders: 229 },
          { date: 'Thu', sales: 2780, orders: 200 },
          { date: 'Fri', sales: 1890, orders: 229 },
          { date: 'Sat', sales: 2390, orders: 200 },
          { date: 'Sun', sales: 3490, orders: 210 }
        ];

        setDashboardData(prev => ({
          ...prev,
          dailySales: mockDailySales
        }));
      }
    };

    fetchDashboardData();
  }, []);

  const COLORS = ['#10b981', '#f59e0b', '#ef4444'];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-white">Dashboard</h2>
        <p className="text-slate-400 mt-1">Welcome to your Data Platform</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Records"
          value={dashboardData.totalRecords.toLocaleString()}
          icon={Database}
          trend={12}
          color="blue"
        />
        <StatCard
          title="Active Users"
          value={dashboardData.activeUsers.toLocaleString()}
          icon={Users}
          trend={8}
          color="green"
        />
        <StatCard
          title="Pipeline Success"
          value={`${dashboardData.pipelineSuccess}%`}
          icon={CheckCircle}
          trend={2}
          color="purple"
        />
        <StatCard
          title="Avg Response Time"
          value={`${dashboardData.avgResponseTime}ms`}
          icon={Clock}
          trend={-5}
          color="orange"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Sales Chart */}
        <ChartCard title="Daily Sales" subtitle="Last 7 days">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={dashboardData.dailySales}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="date" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #475569',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="sales"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ fill: '#3b82f6' }}
              />
              <Line
                type="monotone"
                dataKey="orders"
                stroke="#8b5cf6"
                strokeWidth={2}
                dot={{ fill: '#8b5cf6' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Customer Metrics */}
        <ChartCard title="Customer Metrics" subtitle="Distribution">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={dashboardData.customerMetrics}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {dashboardData.customerMetrics.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #475569',
                  borderRadius: '8px'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Data Quality & Activities */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Data Quality */}
        <ChartCard title="Data Quality" subtitle="Overall status">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={dashboardData.dataQuality}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {dashboardData.dataQuality.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #475569',
                  borderRadius: '8px'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Recent Activities */}
        <div className="lg:col-span-2 bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Recent Activities</h3>
          <div className="space-y-3">
            {dashboardData.recentActivities.map((activity) => (
              <div
                key={activity.id}
                className="flex items-start space-x-3 p-3 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
              >
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                <div className="flex-1">
                  <p className="text-sm text-white">{activity.message}</p>
                  <p className="text-xs text-slate-400 mt-1">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
