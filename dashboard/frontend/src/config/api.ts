/**
 * API Configuration
 *
 * Centralized configuration for API endpoints and settings
 */

// Base API URL - can be overridden by environment variable
export const API_BASE_URL =
	import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

// API Endpoints
export const API_ENDPOINTS = {
	// Health Check
	health: "/health",

	// Price Data
	prices: "/api/prices",
	pricesDateRange: "/api/prices/date-range",
	pricesStatistics: "/api/prices/statistics",
	pricesInfo: "/api/prices/info",

	// Change Points
	changepoints: "/api/changepoints",
	changepointDetail: (id: number) => `/api/changepoints/${id}`,
	changepointsStats: "/api/changepoints/stats",

	// Events
	events: "/api/events",
	eventDetail: (id: number) => `/api/events/${id}`,
	eventImpact: (id: number) => `/api/events/${id}/impact`,
	eventTypes: "/api/events/types",
	eventStats: "/api/events/stats",
} as const;

// Request timeout in milliseconds
export const REQUEST_TIMEOUT = 30000;

// Default date format
export const DATE_FORMAT = "yyyy-MM-dd";

// Chart colors
export const CHART_COLORS = {
	primary: "#2563eb", // Blue for price line
	changepoint: "#ef4444", // Red for change points
	event: "#f59e0b", // Amber for events
	grid: "#e5e7eb", // Gray for grid lines
	text: "#374151", // Dark gray for text
} as const;

// Event type colors
export const EVENT_TYPE_COLORS: Record<string, string> = {
	geopolitical: "#ef4444", // Red
	economic_shock: "#f59e0b", // Amber
	opec_decision: "#10b981", // Green
	sanction: "#8b5cf6", // Purple
} as const;

// Default chart dimensions
export const CHART_CONFIG = {
	defaultHeight: 400,
	defaultMargin: { top: 20, right: 30, left: 60, bottom: 60 },
	animationDuration: 300,
} as const;
