# Brent Oil Change Point Analysis - Frontend

## Overview

Interactive React + TypeScript dashboard for visualizing Brent oil price changes, detected change points, and their correlation with major geopolitical events. Built with modern web technologies and responsive design principles.

## Features

- **Interactive Dashboard**: Real-time data visualization with stats cards, charts, and filters  
- **Price Analysis**: Historical price chart with zoom, pan, and tooltip capabilities
- **Change Point Visualization**: Markers showing detected change points with confidence levels
- **Event Highlighting**: Toggle event markers on timeline to see correlations
- **Detailed Analysis**: Deep-dive page for analyzing specific change points with before/after statistics
- **Event Explorer**: Browse and filter 17+ historical events with advanced search
- **Responsive Design**: Mobile-first approach, works on all screen sizes
- **Type-Safe**: Full TypeScript implementation with comprehensive type definitions

## Technology Stack

- **React 19.2.0** - UI framework
- **TypeScript 5.9.3** - Type-safe development
- **Vite 7.3.1** - Build tool and dev server
- **Tailwind CSS 4.1.18** - Utility-first styling
- **shadcn/ui** - High-quality component library
- **Recharts 3.7.0** - Data visualization
- **Axios 1.13.5** - HTTP client
- **React Router DOM 7.13.0** - Client-side routing
- **date-fns 4.1.0** - Date formatting utilities
- **Lucide React 0.563.0** - Beautiful icons

## Quick Start

```bash
cd dashboard/frontend
pnpm install
pnpm run dev
```

Dashboard available at **http://localhost:5173**

## Installation

### Prerequisites
- Node.js 18.x or higher
- pnpm 10.x or higher (or npm/yarn)
- Backend API running on http://localhost:5000

### Steps

1. **Install Dependencies**
   ```bash
   pnpm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env`:
   ```env
   VITE_API_BASE_URL=http://localhost:5000
   ```

3. **Start Development Server**
   ```bash
   pnpm run dev
   ```

## Available Scripts

```bash
pnpm run dev      # Start development server
pnpm run build    # Build for production
pnpm run preview  # Preview production build
pnpm run lint     # Lint code
```

## Project Structure

```
src/
├── components/
│   ├── ui/          # shadcn UI components
│   ├── common/      # Filters, pickers
│   └── charts/      # PriceChart
├── pages/           # Route pages
│   ├── DetailedAnalysis.tsx
│   ├── EventExplorer.tsx
│   └── About.tsx
├── hooks/           # React hooks (useApi, useData)
├── services/        # API service layer
├── lib/             # API client
├── types/           # TypeScript types
├── config/          # Configuration
├── App.tsx          # Main dashboard
└── main.tsx         # Entry point with routing
```

## Pages

- **Dashboard (/)** - Overview with stats, chart, filters
- **Detailed Analysis (/analysis)** - Change point deep dive
- **Event Explorer (/events)** - Searchable event browser
- **About (/about)** - Methodology and project info

## API Integration

Connects to Flask backend at http://localhost:5000

Key endpoints:
- `GET /api/prices` - Historical prices
- `GET /api/changepoints` - Detected change points
- `GET /api/events` - Historical events
- `GET /health` - API health check

## Troubleshooting

**Port already in use:**
```bash
lsof -ti:5173 | xargs kill -9
```

**API connection failed:**
1. Verify backend running: `curl http://localhost:5000/health`
2. Check `.env` file
3. Ensure CORS enabled on backend

**Build errors:**
```bash
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

---

**Built for Birhan Energies | Part of the Brent Oil Change Point Analysis project**
