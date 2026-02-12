/**
 * Change Point API Service
 *
 * Service functions for fetching change point data from the backend API
 */

import { get } from "../lib/api-client";
import { API_ENDPOINTS } from "../config/api";
import type { ApiResponse, ChangePoint, ChangePointStats } from "../types";

/**
 * Fetch all change points
 * @param minConfidence - Optional minimum confidence threshold (0-1)
 */
export async function fetchChangePoints(
	minConfidence?: number,
): Promise<ApiResponse<ChangePoint[]>> {
	const params = new URLSearchParams();
	if (minConfidence !== undefined) {
		params.append("min_confidence", minConfidence.toString());
	}

	const url = `${API_ENDPOINTS.changepoints}${params.toString() ? `?${params}` : ""}`;
	const response = await get<{ data: ChangePoint[]; count: number }>(url);

	if (response.success && (response as any).data) {
		return {
			success: true,
			data: (response as any).data,
		};
	}

	return response as ApiResponse<ChangePoint[]>;
}

/**
 * Fetch a specific change point by ID
 * @param id - Change point ID
 */
export async function fetchChangePointById(
	id: number,
): Promise<ApiResponse<ChangePoint>> {
	const url = API_ENDPOINTS.changepointDetail(id);
	const response = await get<{ data: ChangePoint }>(url);

	if (response.success && (response as any).data) {
		return {
			success: true,
			data: (response as any).data,
		};
	}

	return response as ApiResponse<ChangePoint>;
}

/**
 * Fetch change point statistics
 */
export async function fetchChangePointStats(): Promise<
	ApiResponse<ChangePointStats>
> {
	const response = await get<{ statistics: ChangePointStats }>(
		API_ENDPOINTS.changepointsStats,
	);

	if (response.success && (response as any).statistics) {
		return {
			success: true,
			data: (response as any).statistics,
		};
	}

	return response as ApiResponse<ChangePointStats>;
}
