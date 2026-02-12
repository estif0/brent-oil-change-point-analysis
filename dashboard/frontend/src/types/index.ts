/**
 * TypeScript Type Definitions
 *
 * All API response and data structure types for the Brent Oil Change Point Analysis Dashboard
 */

// ============================================================================
// API Response Types
// ============================================================================

export interface ApiResponse<T> {
	success: boolean;
	data?: T;
	error?: string;
	message?: string;
}

// ============================================================================
// Price Data Types
// ============================================================================

export interface PriceRecord {
	date: string; // ISO format: "YYYY-MM-DD"
	price: number;
}

export interface PriceStatistics {
	mean: number;
	median: number;
	std: number;
	min: number;
	max: number;
	count: number;
	start_date: string;
	end_date: string;
	percentile_25: number;
	percentile_75: number;
}

export interface DateRange {
	min_date: string;
	max_date: string;
}

export interface DataInfo {
	total_records: number;
	date_range: DateRange;
	columns: string[];
	missing_values: number;
}

// ============================================================================
// Change Point Types
// ============================================================================

export interface ChangePoint {
	id: number;
	date: string;
	mean_before: number;
	mean_after: number;
	std_before: number;
	std_after: number;
	price_change: number;
	percent_change: number;
	confidence: number;
	associated_event: string;
}

export interface ChangePointStats {
	total_count: number;
	by_year: Record<string, number>;
}

// ============================================================================
// Event Types
// ============================================================================

export type EventType =
	| "geopolitical"
	| "economic_shock"
	| "opec_decision"
	| "sanction";
export type ExpectedImpact = "increase" | "decrease" | "mixed";

export interface Event {
	id: number;
	date: string;
	event_name: string;
	event_type: EventType;
	description: string;
	expected_impact: ExpectedImpact;
}

export interface EventImpact {
	event_id: number;
	event_name: string;
	event_date: string;
	window_days: number;
	mean_price_before: number;
	mean_price_after: number;
	price_change: number;
	price_change_pct: number;
	volatility_before: number;
	volatility_after: number;
}

export interface EventStats {
	total_count: number;
	by_type: Record<EventType, number>;
}

// ============================================================================
// Filter Types
// ============================================================================

export interface DateRangeFilter {
	startDate: string | null;
	endDate: string | null;
}

export interface EventFilter {
	eventTypes: EventType[];
	searchQuery: string;
}

export interface ChangePointFilter {
	minConfidence: number;
	year: number | null;
}

// ============================================================================
// Chart Data Types
// ============================================================================

export interface ChartDataPoint {
	date: string;
	price: number;
	isChangePoint?: boolean;
	isEvent?: boolean;
	eventName?: string;
}

export interface TimeSeriesData {
	prices: PriceRecord[];
	changePoints: ChangePoint[];
	events: Event[];
}

// ============================================================================
// UI State Types
// ============================================================================

export interface LoadingState {
	isLoading: boolean;
	error: string | null;
}

export interface DashboardFilters {
	dateRange: DateRangeFilter;
	eventFilter: EventFilter;
	changePointFilter: ChangePointFilter;
}
