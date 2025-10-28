# Data Platform Dashboard - React Frontend

A modern, responsive React-based dashboard for monitoring and managing the Data Platform.

## 🎨 Features

- **Dashboard**: Real-time overview of platform metrics and KPIs
- **Data Quality**: Monitor data quality scores and issues
- **Pipelines**: Track ETL pipeline execution and status
- **Services**: Monitor all platform services and system resources
- **Analytics**: Business metrics and performance analysis
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark Theme**: Eye-friendly dark interface with modern UI

## 🛠️ Technology Stack

- **React 18**: Modern UI library
- **React Router**: Client-side routing
- **Recharts**: Data visualization library
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library
- **Axios**: HTTP client for API calls

## 📦 Installation

### Prerequisites

- Node.js 16+ or Docker

### Local Development

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

### Docker Build

Build the Docker image:
```bash
docker build -t data-platform-frontend:latest .
```

Run the container:
```bash
docker run -p 3000:3000 data-platform-frontend:latest
```

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Sidebar.js          # Navigation sidebar
│   │   ├── Header.js           # Top header with controls
│   │   ├── StatCard.js         # KPI stat card component
│   │   ├── ChartCard.js        # Chart container component
│   │   └── ServiceStatus.js    # Service status indicator
│   ├── pages/
│   │   ├── Dashboard.js        # Main dashboard page
│   │   ├── DataQuality.js      # Data quality monitoring
│   │   ├── Pipelines.js        # Pipeline management
│   │   ├── Services.js         # Services monitoring
│   │   └── Analytics.js        # Business analytics
│   ├── App.js                  # Main app component
│   ├── App.css                 # App styles
│   ├── index.js                # React entry point
│   └── index.css               # Global styles
├── package.json
├── Dockerfile
├── tailwind.config.js
└── README.md
```

## 🎯 Pages Overview

### Dashboard
- Real-time KPIs (Total Records, Active Users, Pipeline Success, Response Time)
- Daily sales trend chart
- Customer metrics distribution
- Data quality overview
- Recent activities feed

### Data Quality
- Overall quality score
- Quality trend analysis
- Table-by-table quality scores
- Data quality issues list with severity levels

### Pipelines
- Pipeline execution status
- Progress tracking
- Task-level details
- Pipeline controls (play, pause, restart)
- Execution history

### Services
- System resource monitoring (CPU, Memory, Disk, Network)
- Service status indicators
- Service details table
- Quick links to all services
- Uptime tracking

### Analytics
- Revenue trends
- Customer segmentation analysis
- Product performance metrics
- Hourly activity patterns
- Top products table

## 🎨 Customization

### Colors and Theme

Edit `tailwind.config.js` to customize colors:

```javascript
theme: {
  extend: {
    colors: {
      // Add custom colors here
    }
  }
}
```

### Adding New Pages

1. Create a new file in `src/pages/`
2. Import and add route in `App.js`
3. Add menu item in `Sidebar.js`

Example:
```javascript
// src/pages/NewPage.js
import React from 'react';

const NewPage = () => {
  return (
    <div className="p-6">
      <h2 className="text-3xl font-bold text-white">New Page</h2>
    </div>
  );
};

export default NewPage;
```

### Connecting to Backend APIs

Update the API calls in each page component:

```javascript
import axios from 'axios';

useEffect(() => {
  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/data');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  fetchData();
}, []);
```

## 🚀 Deployment

### Docker Compose

The frontend is included in the main `docker-compose.yml`:

```bash
docker-compose up -d frontend
```

### Production Build

Create an optimized production build:

```bash
npm run build
```

The build folder contains the optimized production files.

### Environment Variables

Create a `.env` file for environment-specific configuration:

```env
REACT_APP_API_URL=http://api.example.com
REACT_APP_ENV=production
```

## 📊 Data Integration

The dashboard currently uses mock data. To integrate with real data:

1. Create API endpoints in your backend
2. Update the `useEffect` hooks in each page
3. Replace mock data with API calls

Example API structure:
```
GET /api/dashboard/stats
GET /api/data-quality/metrics
GET /api/pipelines/status
GET /api/services/status
GET /api/analytics/revenue
```

## 🔧 Available Scripts

### `npm start`
Runs the app in development mode at `http://localhost:3000`

### `npm run build`
Builds the app for production to the `build` folder

### `npm test`
Launches the test runner

### `npm run eject`
Ejects from Create React App (irreversible)

## 📚 Dependencies

- **react**: ^18.2.0 - UI library
- **react-dom**: ^18.2.0 - React DOM rendering
- **react-router-dom**: ^6.20.0 - Routing
- **axios**: ^1.6.0 - HTTP client
- **recharts**: ^2.10.0 - Charts
- **lucide-react**: ^0.294.0 - Icons
- **tailwindcss**: ^3.3.0 - CSS framework
- **date-fns**: ^2.30.0 - Date utilities

## 🐛 Troubleshooting

### Port 3000 already in use
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

### Dependencies not installing
```bash
rm -rf node_modules package-lock.json
npm install
```

### Docker build fails
```bash
docker build --no-cache -t data-platform-frontend:latest .
```

## 📖 Resources

- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Recharts Documentation](https://recharts.org)
- [React Router Documentation](https://reactrouter.com)

## 📝 License

This project is part of the Data Platform demonstrator.

## 🤝 Contributing

To contribute improvements:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

**Last Updated**: 2024
**Version**: 1.0.0
