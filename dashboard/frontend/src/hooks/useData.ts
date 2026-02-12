/**
 * Custom hooks for specific data fetching
 */

import { useQuery } from "./useApi";
import {
	fetchPrices,
	fetchPriceStatistics,
	fetchDateRange,
	fetchDataInfo,
} from "../services/data.service";
import {
	fetchChangePoints,
	fetchChangePointById,
	fetchChangePointStats,
} from "../services/changepoint.service";
import {
	fetchEvents,
	fetchEventById,
	fetchEventImpact,
	fetchEventTypes,
	fetchEventStats,
} from "../services/event.service";
import type {
	PriceRecord,
	PriceStatistics,
	DateRange,
	DataInfo,
	ChangePoint,
	ChangePointStats,
	Event,
	EventType,
	EventImpact,
	EventStats,
} from "../types";

// ============================================================================
// Price Data Hooks
// ============================================================================

export function usePrices(startDate?: string, endDate?: string) {
	return useQuery<PriceRecord[]>(
		() => fetchPrices(startDate, endDate),
		[startDate, endDate],
	);
}

export function usePriceStatistics(startDate?: string, endDate?: string) {
	return useQuery<PriceStatistics>(
		() => fetchPriceStatistics(startDate, endDate),
		[startDate, endDate],
	);
}

export function useDateRange() {
	return useQuery<DateRange>(() => fetchDateRange(), []);
}

export function useDataInfo() {
	return useQuery<DataInfo>(() => fetchDataInfo(), []);
}

// ============================================================================
// Change Point Hooks
// ============================================================================

export function useChangePoints(minConfidence?: number) {
	return useQuery<ChangePoint[]>(
		() => fetchChangePoints(minConfidence),
		[minConfidence],
	);
}

export function useChangePoint(id: number) {
	return useQuery<ChangePoint>(() => fetchChangePointById(id), [id]);
}

export function useChangePointStats() {
	return useQuery<ChangePointStats>(() => fetchChangePointStats(), []);
}

// ============================================================================
// Event Hooks
// ============================================================================

export function useEvents(eventType?: EventType) {
	return useQuery<Event[]>(() => fetchEvents(eventType), [eventType]);
}

export function useEvent(id: number) {
	return useQuery<Event>(() => fetchEventById(id), [id]);
}

export function useEventImpact(id: number, windowDays: number = 30) {
	return useQuery<EventImpact>(
		() => fetchEventImpact(id, windowDays),
		[id, windowDays],
	);
}

export function useEventTypes() {
	return useQuery<EventType[]>(() => fetchEventTypes(), []);
}

export function useEventStats() {
	return useQuery<EventStats>(() => fetchEventStats(), []);
}
