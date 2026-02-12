# Brent Oil Change Point Analysis - Frontend

React + TypeScript + Vite dashboard for visualizing Brent oil price change points and the impact of major geopolitical and economic events.

## 🚀 Quick Start

```bash
# Install dependencies
pnpm install

# Start development server
pnpm run dev

# Build for production
pnpm run build
```

## 📦 Tech Stack

- **Framework:** React 19 + TypeScript  
- **Build Tool:** Vite 7
- **Styling:** Tailwind CSS 4
- **Charts:** Recharts
- **HTTP Client:** Axios
- **Routing:** React Router DOM (planned)
- **Icons:** Lucide React
- **Date Utils:** date-fns

## 📁 Project Structure

```
src/
├── components/ui/      # Reusable UI components
├── config/            # Configuration & constants
├── hooks/             # Custom React hooks
├── lib/               # Utility libraries
├── services/          # API service layer
├── types/             # TypeScript definitions
├── App.tsx           # Main component
└── main.tsx          # Entry point
```

## ✅ Currently Implemented

- **API Integration** - Full REST API client with error handling
- **Type Safety** - Complete TypeScript coverage
- **Custom Hooks** - Reusable data fetching (`useQuery`, `useLazyQuery`)
- **UI Components** - Card, LoadingSpinner, ErrorDisplay
- **Dashboard Overview** - Stats cards for data range, change points, events
- **Health Check** - API connection status indicator
- **Responsive Design** - Mobile-friendly Tailwind layout
- **Change Point Display** - Detected change points with confidence
- **Event Cards** - Major events with type badges

## 🔜 Coming Next

- Interactive charts with Recharts
- Date range filters
- Event impact visualizations
- Multi-page routing
- Advanced filtering options
- Export features (CSV/PNG)

## 🔌 API Endpoints

### Price Data
- `GET /api/prices` - Historical prices
- `GET /api/prices/statistics` - Statistics
- `GET /api/prices/date-range` - Date range
- `GET /api/prices/info` - Metadata

### Change Points
- `GET /api/changepoints` - All change points
- `GET /api/changepoints/:id` - Specific change point
- `GET /api/changepoints/stats` - Statistics

### Events
- `GET /api/events` - All events
- `GET /api/events/:id` - Specific event
- `GET /api/events/:id/impact` - Impact analysis
- `GET /api/events/types` - Event types
- `GET /api/events/stats` - Statistics

## 🪝 Custom Hooks

```tsx
// Generic data fetching
const { data, loading, error, refetch } = useQuery(
  () => fetchPrices('2020-01-01', '2020-12-31'),
  ['2020-01-01', '2020-12-31']
);

// Specific hooks
const { data: prices } = usePrices(startDate, endDate);
const { data: changePoints } = useChangePoints(minConfidence);
const { data: events } = useEvents(eventType);
```

## 🎨 UI Components

```tsx
<Card title="My Title">
  <p>Content</p>
</Card>

<LoadingSpinner size="md" />

<ErrorDisplay error="Error message" onRetry={refetch} />
```

## ⚙️ Environment Variables

Create a `.env` file:

```env
VITE_API_BASE_URL=http://localhost:5000
```

## 🐛 Troubleshooting

**API Connection Issues:**
```bash
# Check backend health
curl http://localhost:5000/health

# Verify .env configuration
cat .env
```

**Build Errors:**
```bash
# Clear and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## 📸 Current Dashboard

The dashboard displays:
- **API Health Status** - Real-time connection indicator
- **Stats Grid** - Data range (1987-2022), 1 change point, 17 events
- **Change Point Card** - 2008-07-14 detection with 94% confidence  
- **Event Preview** - Major events like Gulf War, Financial Crisis, etc.

## 📄 License

Part of the Brent Oil Change Point Analysis project © 2026 Birhan Energies
