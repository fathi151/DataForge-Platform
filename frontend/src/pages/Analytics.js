import React, { useState, useEffect } from 'react';
import {
  AreaChart,
  Area,
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
import { TrendingUp, Users, ShoppingCart, DollarSign } from 'lucide-react';

const Analytics = () => {
  const [analyticsData, setAnalyticsData] = useState({
    totalRevenue: 125430,
    totalOrders: 3240,
    avgOrderValue: 38.7,
    conversionRate: 3.2,
    revenueTrend: [],
    customerSegmentation: [],
    productPerformance: [],
    hourlyActivity: []
  });

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      try {
        // Fetch revenue analytics
        const revenueResponse = await fetch('http://localhost:8000/api/analytics/revenue');
        const revenueData = await revenueResponse.json();

        // Fetch customer analytics
        const customerResponse = await fetch('http://localhost:8000/api/analytics/customers');
        const customerData = await customerResponse.json();

        // Format revenue trend
        const revenueTrend = revenueData.revenueTrend.map(item => ({
          date: new Date(item.date).toLocaleDateString('en-US'),
          revenue: parseFloat(item.revenue) || 0,
          orders: item.orders || 0
        }));

        // Customer segmentation (from customer data)
        const customerSegmentation = [
          { segment: 'All Customers', customers: customerData.totalCustomers, revenue: revenueData.totalRevenue }
        ];

        // Product performance (mock for now - can be extended with real data)
        const productPerformance = [
          { product: 'All Products', sales: revenueData.totalOrders, revenue: revenueData.totalRevenue }
        ];

        // Hourly activity (mock - would need additional API endpoint)
        const hourlyActivity = [
          { hour: '00:00', activity: 120 },
          { hour: '04:00', activity: 80 },
          { hour: '08:00', activity: 450 },
          { hour: '12:00', activity: 890 },
          { hour: '16:00', activity: 1200 },
          { hour: '20:00', activity: 950 },
          { hour: '23:00', activity: 300 }
        ];

        setAnalyticsData({
          totalRevenue: revenueData.totalRevenue,
          totalOrders: revenueData.totalOrders,
          avgOrderValue: revenueData.avgOrderValue,
          conversionRate: revenueData.conversionRate,
          revenueTrend: revenueTrend,
          customerSegmentation: customerSegmentation,
          productPerformance: productPerformance,
          hourlyActivity: hourlyActivity
        });
      } catch (error) {
        console.error('Error fetching analytics data:', error);
      }
    };

    fetchAnalyticsData();
  }, []);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-white">Analytics</h2>
        <p className="text-slate-400 mt-1">Business metrics and performance analysis</p>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Revenue"
          value={`$${analyticsData.totalRevenue.toLocaleString()}`}
          icon={DollarSign}
          trend={15}
          color="green"
        />
        <StatCard
          title="Total Orders"
          value={analyticsData.totalOrders.toLocaleString()}
          icon={ShoppingCart}
          trend={12}
          color="blue"
        />
        <StatCard
          title="Avg Order Value"
          value={`$${analyticsData.avgOrderValue}`}
          icon={TrendingUp}
          trend={8}
          color="purple"
        />
        <StatCard
          title="Conversion Rate"
          value={`${analyticsData.conversionRate}%`}
          icon={Users}
          trend={3}
          color="orange"
        />
      </div>

      {/* Revenue Trend */}
      <ChartCard title="Revenue Trend" subtitle="Last 6 days">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={analyticsData.revenueTrend}>
            <defs>
              <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
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
            <Area
              type="monotone"
              dataKey="revenue"
              stroke="#3b82f6"
              fillOpacity={1}
              fill="url(#colorRevenue)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Customer Segmentation */}
        <ChartCard title="Customer Segmentation" subtitle="By segment">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={analyticsData.customerSegmentation}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="segment" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #475569',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Bar dataKey="customers" fill="#3b82f6" />
              <Bar dataKey="revenue" fill="#8b5cf6" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Hourly Activity */}
        <ChartCard title="Hourly Activity" subtitle="User activity by hour">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={analyticsData.hourlyActivity}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="hour" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #475569',
                  borderRadius: '8px'
                }}
              />
              <Line
                type="monotone"
                dataKey="activity"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ fill: '#10b981' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Product Performance */}
      <ChartCard title="Product Performance" subtitle="Sales and revenue by product">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={analyticsData.productPerformance}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="product" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px'
              }}
            />
            <Legend />
            <Bar dataKey="sales" fill="#3b82f6" />
            <Bar dataKey="revenue" fill="#10b981" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Summary Table */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">Top Products</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Product</th>
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Sales</th>
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Revenue</th>
                <th className="text-left py-3 px-4 text-slate-300 font-medium">Growth</th>
              </tr>
            </thead>
            <tbody>
              {analyticsData.productPerformance.map((product, index) => (
                <tr key={index} className="border-b border-slate-700 hover:bg-slate-700/50 transition-colors">
                  <td className="py-3 px-4 text-white font-medium">{product.product}</td>
                  <td className="py-3 px-4 text-slate-300">{product.sales.toLocaleString()}</td>
                  <td className="py-3 px-4 text-slate-300">${product.revenue.toLocaleString()}</td>
                  <td className="py-3 px-4">
                    <span className="text-green-400 font-medium">+{Math.floor(Math.random() * 30)}%</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
