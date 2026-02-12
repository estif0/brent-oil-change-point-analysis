/**
 * Event API Service
 *
 * Service functions for fetching event data from the backend API
 */

import { get } from "../lib/api-client";
import { API_ENDPOINTS } from "../config/api";
import type {
	ApiResponse,
	Event,
	EventType,
	EventImpact,
	EventStats,
} from "../types";

/**
 * Fetch all events
 * @param eventType - Optional filter by event type
 */
export async function fetchEvents(
	eventType?: EventType,
): Promise<ApiResponse<Event[]>> {
	const params = new URLSearchParams();
	if (eventType) {
		params.append("event_type", eventType);
	}

	const url = `${API_ENDPOINTS.events}${params.toString() ? `?${params}` : ""}`;
	const response = await get<{ data: Event[]; count: number }>(url);

	if (response.success && (response as any).data) {
		return {
			success: true,
			data: (response as any).data,
		};
	}

	return response as ApiResponse<Event[]>;
}

/**
 * Fetch a specific event by ID
 * @param id - Event ID
 */
export async function fetchEventById(id: number): Promise<ApiResponse<Event>> {
	const url = API_ENDPOINTS.eventDetail(id);
	const response = await get<{ data: Event }>(url);

	if (response.success && (response as any).data) {
		return {
			success: true,
			data: (response as any).data,
		};
	}

	return response as ApiResponse<Event>;
}

/**
 * Fetch event impact analysis
 * @param id - Event ID
 * @param windowDays - Number of days before/after event to analyze (default: 30)
 */
export async function fetchEventImpact(
	id: number,
	windowDays: number = 30,
): Promise<ApiResponse<EventImpact>> {
	const params = new URLSearchParams();
	params.append("window_days", windowDays.toString());

	const url = `${API_ENDPOINTS.eventImpact(id)}?${params}`;
	const response = await get<{ impact: EventImpact }>(url);

	if (response.success && (response as any).impact) {
		return {
			success: true,
			data: (response as any).impact,
		};
	}

	return response as ApiResponse<EventImpact>;
}

/**
 * Fetch available event types
 */
export async function fetchEventTypes(): Promise<ApiResponse<EventType[]>> {
	const response = await get<{ event_types: EventType[] }>(
		API_ENDPOINTS.eventTypes,
	);

	if (response.success && (response as any).event_types) {
		return {
			success: true,
			data: (response as any).event_types,
		};
	}

	return response as ApiResponse<EventType[]>;
}

/**
 * Fetch event statistics
 */
export async function fetchEventStats(): Promise<ApiResponse<EventStats>> {
	const response = await get<{ statistics: EventStats }>(
		API_ENDPOINTS.eventStats,
	);

	if (response.success && (response as any).statistics) {
		return {
			success: true,
			data: (response as any).statistics,
		};
	}

	return response as ApiResponse<EventStats>;
}
