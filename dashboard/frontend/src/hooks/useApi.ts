/**
 * Custom React Hooks for Data Fetching
 *
 * Reusable hooks for fetching data from the API with loading and error states
 */

import { useState, useEffect, useCallback } from "react";
import type { ApiResponse } from "../types";

/**
 * Loading and error state interface
 */
interface UseQueryState<T> {
	data: T | null;
	loading: boolean;
	error: string | null;
	refetch: () => Promise<void>;
}

/**
 * Generic hook for fetching data from API
 * @param fetcher - Function that returns a promise with API response
 * @param dependencies - Array of dependencies that trigger refetch
 */
export function useQuery<T>(
	fetcher: () => Promise<ApiResponse<T>>,
	dependencies: unknown[] = [],
): UseQueryState<T> {
	const [data, setData] = useState<T | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);

	const fetchData = useCallback(async () => {
		setLoading(true);
		setError(null);

		try {
			const response = await fetcher();

			if (response.success && response.data) {
				setData(response.data);
				setError(null);
			} else {
				setError(response.error || "Failed to fetch data");
				setData(null);
			}
		} catch (err) {
			setError(
				err instanceof Error
					? err.message
					: "An unknown error occurred",
			);
			setData(null);
		} finally {
			setLoading(false);
		}
	}, [fetcher]);

	useEffect(() => {
		let isMounted = true;

		const loadData = async () => {
			setLoading(true);
			setError(null);

			try {
				const response = await fetcher();

				if (isMounted) {
					if (response.success && response.data) {
						setData(response.data);
						setError(null);
					} else {
						setError(response.error || "Failed to fetch data");
						setData(null);
					}
				}
			} catch (err) {
				if (isMounted) {
					setError(
						err instanceof Error
							? err.message
							: "An unknown error occurred",
					);
					setData(null);
				}
			} finally {
				if (isMounted) {
					setLoading(false);
				}
			}
		};

		loadData();

		return () => {
			isMounted = false;
		};
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [...dependencies]);

	return {
		data,
		loading,
		error,
		refetch: fetchData,
	};
}

/**
 * Hook for lazy data fetching (manual trigger)
 */
export function useLazyQuery<T>(): {
	data: T | null;
	loading: boolean;
	error: string | null;
	fetch: (fetcher: () => Promise<ApiResponse<T>>) => Promise<void>;
} {
	const [data, setData] = useState<T | null>(null);
	const [loading, setLoading] = useState<boolean>(false);
	const [error, setError] = useState<string | null>(null);

	const fetch = async (fetcher: () => Promise<ApiResponse<T>>) => {
		setLoading(true);
		setError(null);

		try {
			const response = await fetcher();

			if (response.success && response.data) {
				setData(response.data);
				setError(null);
			} else {
				setError(response.error || "Failed to fetch data");
				setData(null);
			}
		} catch (err) {
			setError(
				err instanceof Error
					? err.message
					: "An unknown error occurred",
			);
			setData(null);
		} finally {
			setLoading(false);
		}
	};

	return {
		data,
		loading,
		error,
		fetch,
	};
}
