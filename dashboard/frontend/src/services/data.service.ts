/**
 * Data API Service
 *
 * Service functions for fetching price data from the backend API
 */

import { get } from "../lib/api-client";
import { API_ENDPOINTS } from "../config/api";
import type {
	ApiResponse,
	PriceRecord,
	PriceStatistics,
	DateRange,
	DataInfo,
} from "../types";

/**
 * Fetch historical price data
 * @param startDate - Optional start date (YYYY-MM-DD)
 * @param endDate - Optional end date (YYYY-MM-DD)
 */
export async function fetchPrices(
	startDate?: string,
	endDate?: string,
): Promise<ApiResponse<PriceRecord[]>> {
	const params = new URLSearchParams();
	if (startDate) params.append("start_date", startDate);
	if (endDate) params.append("end_date", endDate);

	const url = `${API_ENDPOINTS.prices}${params.toString() ? `?${params}` : ""}`;
	const response = await get<{ data: PriceRecord[]; count: number }>(url);

	if (response.success && (response as any).data) {
		return {
			success: true,
			data: (response as any).data,
		};
	}

	return response as ApiResponse<PriceRecord[]>;
}

/**
 * Fetch price statistics for a date range
 * @param startDate - Optional start date (YYYY-MM-DD)
 * @param endDate - Optional end date (YYYY-MM-DD)
 */
export async function fetchPriceStatistics(
	startDate?: string,
	endDate?: string,
): Promise<ApiResponse<PriceStatistics>> {
	const params = new URLSearchParams();
	if (startDate) params.append("start_date", startDate);
	if (endDate) params.append("end_date", endDate);

	const url = `${API_ENDPOINTS.pricesStatistics}${params.toString() ? `?${params}` : ""}`;
	const response = await get<{ statistics: PriceStatistics }>(url);

	if (response.success && (response as any).statistics) {
		return {
			success: true,
			data: (response as any).statistics,
		};
	}

	return response as ApiResponse<PriceStatistics>;
}

/**
 * Fetch available date range
 */
export async function fetchDateRange(): Promise<ApiResponse<DateRange>> {
	const response = await get<{ date_range: DateRange }>(
		API_ENDPOINTS.pricesDateRange,
	);

	if (response.success && (response as any).date_range) {
		return {
			success: true,
			data: (response as any).date_range,
		};
	}

	return response as ApiResponse<DateRange>;
}

/**
 * Fetch data info (metadata)
 */
export async function fetchDataInfo(): Promise<ApiResponse<DataInfo>> {
	const response = await get<{ info: DataInfo }>(API_ENDPOINTS.pricesInfo);

	if (response.success && (response as any).info) {
		return {
			success: true,
			data: (response as any).info,
		};
	}

	return response as ApiResponse<DataInfo>;
}
