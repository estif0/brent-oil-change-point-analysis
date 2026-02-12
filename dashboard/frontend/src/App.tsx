/**
 * Main App Component
 *
 * Brent Oil Change Point Analysis Dashboard
 */

import { useEffect, useState, useMemo } from "react";
import { Activity, TrendingUp, Calendar, AlertTriangle } from "lucide-react";
import {
	LoadingSpinner,
	ErrorDisplay,
	Card,
	ToggleSwitch,
} from "./components/ui";
import { PriceChart } from "./components/charts";
import { DateRangePicker, FilterDropdown } from "./components/common";
import {
	useChangePoints,
	useEvents,
	useDateRange,
	usePrices,
} from "./hooks/useData";
import { checkHealth } from "./lib/api-client";

function App() {
	const [apiHealthy, setApiHealthy] = useState<boolean | null>(null);
	const [showChangePoints, setShowChangePoints] = useState(true);
	const [showEvents, setShowEvents] = useState(true);
	const [showAllEvents, setShowAllEvents] = useState(false);

	// Filter states
	const [startDate, setStartDate] = useState<string>("");
	const [endDate, setEndDate] = useState<string>("");
	const [selectedEventTypes, setSelectedEventTypes] = useState<string[]>([]);

	// Fetch data using custom hooks
	const {
		data: dateRange,
		loading: dateLoading,
		error: dateError,
	} = useDateRange();
	const {
		data: changePoints,
		loading: cpLoading,
		error: cpError,
	} = useChangePoints();
	const {
		data: events,
		loading: eventsLoading,
		error: eventsError,
	} = useEvents();
	const {
		data: prices,
		loading: pricesLoading,
		error: pricesError,
	} = usePrices(startDate || undefined, endDate || undefined);

	// Initialize date range filters once when dateRange is available
	useEffect(() => {
		if (dateRange && !startDate && !endDate) {
			setStartDate(dateRange.min_date);
			setEndDate(dateRange.max_date);
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [dateRange]); // Only depend on dateRange to avoid cascading renders

	// Check API health on mount
	useEffect(() => {
		checkHealth().then(setApiHealthy);
	}, []);

	// Get unique event types
	const eventTypes = useMemo(() => {
		if (!events) return [];
		const types = new Set(events.map((e) => e.event_type));
		return Array.from(types);
	}, [events]);

	// Filter events by selected types
	const filteredEvents = useMemo(() => {
		if (!events) return [];
		if (selectedEventTypes.length === 0) return events;
		return events.filter((e) => selectedEventTypes.includes(e.event_type));
	}, [events, selectedEventTypes]);

	// Filter events by date range
	const dateFilteredEvents = useMemo(() => {
		if (!filteredEvents || !startDate || !endDate) return filteredEvents;
		return filteredEvents.filter(
			(e) => e.date >= startDate && e.date <= endDate,
		);
	}, [filteredEvents, startDate, endDate]);

	// Handle event type toggle
	const handleEventTypeToggle = (type: string) => {
		setSelectedEventTypes((prev) =>
			prev.includes(type)
				? prev.filter((t) => t !== type)
				: [...prev, type],
		);
	};

	return (
		<div className="bg-gray-50 min-h-screen">
			{/* Header */}
			<header className="bg-white shadow-sm border-gray-200 border-b">
				<div className="mx-auto px-4 sm:px-6 lg:px-8 py-6 max-w-7xl">
					<div className="flex justify-between items-center">
						<div>
							<h1 className="font-bold text-gray-900 text-3xl">
								Brent Oil Change Point Analysis
							</h1>
							<p className="mt-1 text-gray-600 text-sm">
								Analyzing the impact of major events on Brent
								crude oil prices
							</p>
						</div>
						<div className="flex items-center gap-2">
							<span
								className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
									apiHealthy
										? "bg-green-100 text-green-800"
										: apiHealthy === false
											? "bg-red-100 text-red-800"
											: "bg-gray-100 text-gray-800"
								}`}
							>
								<span
									className={`w-2 h-2 rounded-full mr-2 ${
										apiHealthy
											? "bg-green-500"
											: apiHealthy === false
												? "bg-red-500"
												: "bg-gray-500"
									}`}
								/>
								{apiHealthy
									? "API Connected"
									: apiHealthy === false
										? "API Offline"
										: "Checking..."}
							</span>
						</div>
					</div>
				</div>
			</header>

			{/* Main Content */}
			<main className="mx-auto px-4 sm:px-6 lg:px-8 py-8 max-w-7xl">
				{/* Stats Grid */}
				<div className="gap-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 mb-8">
					{/* Date Range Card */}
					<Card>
						<div className="flex justify-between items-center">
							<div>
								<p className="font-medium text-gray-600 text-sm">
									Data Range
								</p>
								{dateLoading ? (
									<LoadingSpinner
										size="sm"
										className="mt-2"
									/>
								) : dateError ? (
									<p className="mt-1 text-red-600 text-xs">
										{dateError}
									</p>
								) : dateRange ? (
									<div className="mt-2">
										<p className="text-gray-500 text-xs">
											{dateRange.min_date}
										</p>
										<p className="text-gray-500 text-xs">
											to
										</p>
										<p className="text-gray-500 text-xs">
											{dateRange.max_date}
										</p>
									</div>
								) : null}
							</div>
							<Calendar className="w-8 h-8 text-blue-600" />
						</div>
					</Card>

					{/* Change Points Card */}
					<Card>
						<div className="flex justify-between items-center">
							<div>
								<p className="font-medium text-gray-600 text-sm">
									Change Points
								</p>
								{cpLoading ? (
									<LoadingSpinner
										size="sm"
										className="mt-2"
									/>
								) : cpError ? (
									<p className="mt-1 text-red-600 text-xs">
										{cpError}
									</p>
								) : changePoints ? (
									<p className="mt-2 font-bold text-gray-900 text-2xl">
										{changePoints.length}
									</p>
								) : null}
							</div>
							<Activity className="w-8 h-8 text-red-600" />
						</div>
					</Card>

					{/* Events Card */}
					<Card>
						<div className="flex justify-between items-center">
							<div>
								<p className="font-medium text-gray-600 text-sm">
									Major Events
								</p>
								{eventsLoading ? (
									<LoadingSpinner
										size="sm"
										className="mt-2"
									/>
								) : eventsError ? (
									<p className="mt-1 text-red-600 text-xs">
										{eventsError}
									</p>
								) : events ? (
									<p className="mt-2 font-bold text-gray-900 text-2xl">
										{events.length}
									</p>
								) : null}
							</div>
							<AlertTriangle className="w-8 h-8 text-amber-600" />
						</div>
					</Card>

					{/* Status Card */}
					<Card>
						<div className="flex justify-between items-center">
							<div>
								<p className="font-medium text-gray-600 text-sm">
									Status
								</p>
								<p className="mt-2 font-bold text-green-600 text-2xl">
									Ready
								</p>
							</div>
							<TrendingUp className="w-8 h-8 text-green-600" />
						</div>
					</Card>
				</div>

				{/* Filters Section */}
				<Card
					title="Filters & Controls"
					className="bg-linear-to-br from-white to-gray-50 mb-8"
				>
					<div className="space-y-6">
						{/* Date Range Filter */}
						<div className="bg-white p-4 border border-gray-100 rounded-lg">
							<h3 className="mb-3 font-semibold text-gray-700 text-sm">
								Date Range
							</h3>
							<DateRangePicker
								startDate={startDate}
								endDate={endDate}
								onStartDateChange={setStartDate}
								onEndDateChange={setEndDate}
								availableRange={dateRange || undefined}
							/>
						</div>

						{/* Event Type Filter */}
						{eventTypes.length > 0 && (
							<div className="bg-white p-4 border border-gray-100 rounded-lg">
								<FilterDropdown
									label="Event Types"
									options={eventTypes}
									selectedOptions={selectedEventTypes}
									onToggle={handleEventTypeToggle}
									onReset={() => setSelectedEventTypes([])}
								/>
							</div>
						)}

						{/* Chart Toggles */}
						<div className="bg-white p-4 border border-gray-100 rounded-lg">
							<div className="flex items-center gap-4">
								<span className="font-semibold text-gray-700 text-sm">
									Chart Display:
								</span>
								<ToggleSwitch
									enabled={showChangePoints}
									onChange={setShowChangePoints}
									label="Change Points"
									size="sm"
								/>
								<ToggleSwitch
									enabled={showEvents}
									onChange={setShowEvents}
									label="Events"
									size="sm"
								/>
							</div>
						</div>
					</div>
				</Card>

				{/* Interactive Price Chart */}
				<Card title="Brent Oil Price History" className="mb-8">
					{pricesLoading ? (
						<div className="flex justify-center items-center h-96">
							<LoadingSpinner size="lg" />
						</div>
					) : pricesError ? (
						<ErrorDisplay error={pricesError} />
					) : prices && prices.length > 0 ? (
						<>
							<div className="flex sm:flex-row flex-col justify-between items-start sm:items-center gap-4 mb-6">
								<div className="space-y-1 text-gray-600 text-sm">
									<p>
										Showing{" "}
										<span className="font-semibold">
											{prices.length}
										</span>{" "}
										data points
										{startDate && endDate && (
											<>
												{" "}
												from {startDate} to {endDate}
											</>
										)}
									</p>
									{dateFilteredEvents && (
										<p>
											<span className="font-semibold">
												{dateFilteredEvents.length}
											</span>{" "}
											events in selected range
											{selectedEventTypes.length > 0 && (
												<>
													{" "}
													(filtered by{" "}
													{
														selectedEventTypes.length
													}{" "}
													type
													{selectedEventTypes.length >
													1
														? "s"
														: ""}
													)
												</>
											)}
										</p>
									)}
								</div>

								{/* Chart Legend */}
								<div className="flex items-center gap-4 bg-gray-50 px-4 py-2 border border-gray-200 rounded-lg text-xs">
									<div className="flex items-center gap-1.5">
										<div className="bg-blue-600 w-8 h-0.5"></div>
										<span className="text-gray-600">
											Price
										</span>
									</div>
									{showChangePoints && (
										<div className="flex items-center gap-1.5">
											<div className="bg-red-600 border-t-2 border-dashed w-8 h-0.5"></div>
											<span className="text-gray-600">
												Change Points
											</span>
										</div>
									)}
									{showEvents && (
										<div className="flex items-center gap-1.5">
											<div className="bg-amber-600 border-t border-dashed w-8 h-0.5"></div>
											<span className="text-gray-600">
												Events
											</span>
										</div>
									)}
								</div>
							</div>
							<PriceChart
								data={prices}
								changePoints={changePoints || []}
								events={dateFilteredEvents || []}
								showChangePoints={showChangePoints}
								showEvents={showEvents}
								height={500}
							/>
						</>
					) : (
						<div className="py-12 text-center">
							<p className="mb-2 text-gray-500">
								No price data available for the selected range
							</p>
							<button
								onClick={() => {
									if (dateRange) {
										setStartDate(dateRange.min_date);
										setEndDate(dateRange.max_date);
									}
								}}
								className="font-medium text-blue-600 hover:text-blue-800 text-sm"
							>
								Reset filters
							</button>
						</div>
					)}
				</Card>

				{/* Change Points Section */}
				{changePoints && changePoints.length > 0 && (
					<Card title="Detected Change Points" className="mb-8">
						<p className="mb-4 text-gray-600 text-sm">
							Bayesian change point detection identified
							significant shifts in price behavior at the
							following dates.
						</p>
						<div className="space-y-4">
							{changePoints.map((cp) => (
								<div
									key={cp.id}
									className="bg-linear-to-br from-white to-gray-50 hover:shadow-lg p-6 border border-gray-200 hover:border-blue-200 rounded-lg transition-all duration-200"
								>
									<div className="flex justify-between items-start">
										<div className="flex-1">
											<div className="flex items-center gap-3 mb-3">
												<div className="flex justify-center items-center bg-red-100 rounded-full w-10 h-10">
													<Activity className="w-5 h-5 text-red-600" />
												</div>
												<div>
													<h3 className="font-bold text-gray-900 text-lg">
														{cp.date}
													</h3>
													<span className="bg-blue-100 px-3 py-1 rounded-full font-semibold text-blue-800 text-xs">
														{(
															cp.confidence * 100
														).toFixed(0)}
														% confidence
													</span>
												</div>
											</div>
											<p className="mb-2 text-gray-600 text-sm">
												<strong>
													Associated Event:
												</strong>{" "}
												{cp.associated_event}
											</p>
											<div className="gap-4 grid grid-cols-2 text-sm">
												<div>
													<p className="text-gray-500">
														Mean Before
													</p>
													<p className="font-medium">
														{cp.mean_before.toFixed(
															6,
														)}
													</p>
												</div>
												<div>
													<p className="text-gray-500">
														Mean After
													</p>
													<p className="font-medium">
														{cp.mean_after.toFixed(
															6,
														)}
													</p>
												</div>
												<div>
													<p className="text-gray-500">
														Volatility Before
													</p>
													<p className="font-medium">
														{cp.std_before.toFixed(
															6,
														)}
													</p>
												</div>
												<div>
													<p className="text-gray-500">
														Volatility After
													</p>
													<p className="font-medium">
														{cp.std_after.toFixed(
															6,
														)}
													</p>
												</div>
											</div>
										</div>
									</div>
								</div>
							))}
						</div>
					</Card>
				)}

				{/* Events Section */}
				{dateFilteredEvents && dateFilteredEvents.length > 0 ? (
					<Card title="Major Events" className="mb-8">
						<div className="flex justify-between items-center mb-4">
							<p className="text-gray-600 text-sm">
								Historical events that may have influenced Brent
								oil prices.
								{selectedEventTypes.length > 0 && (
									<>
										{" "}
										Filtered by:{" "}
										<span className="font-semibold">
											{selectedEventTypes.join(", ")}
										</span>
									</>
								)}
							</p>
							{dateFilteredEvents.length > 6 && (
								<button
									onClick={() =>
										setShowAllEvents(!showAllEvents)
									}
									className="font-medium text-blue-600 hover:text-blue-800 text-sm"
								>
									{showAllEvents
										? "Show Less"
										: `Show All (${dateFilteredEvents.length})`}
								</button>
							)}
						</div>
						<div className="gap-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
							{(showAllEvents
								? dateFilteredEvents
								: dateFilteredEvents.slice(0, 6)
							).map((event) => (
								<div
									key={event.id}
									className="bg-white hover:shadow-lg p-5 border border-gray-200 hover:border-blue-200 rounded-lg hover:scale-105 transition-all duration-200 cursor-pointer"
								>
									<div className="flex justify-between items-start mb-3">
										<h4 className="font-bold text-gray-900 text-sm leading-tight">
											{event.event_name}
										</h4>
										<span
											className={`px-2.5 py-1 text-xs font-semibold rounded-full shrink-0 ml-2 ${
												event.event_type ===
												"geopolitical"
													? "bg-red-100 text-red-700"
													: event.event_type ===
														  "economic_shock"
														? "bg-amber-100 text-amber-700"
														: event.event_type ===
															  "opec_decision"
															? "bg-green-100 text-green-700"
															: "bg-purple-100 text-purple-700"
											}`}
										>
											{event.event_type.replace("_", " ")}
										</span>
									</div>
									<p className="flex items-center gap-1 mb-3 font-semibold text-gray-500 text-xs">
										<Calendar className="w-3 h-3" />
										{event.date}
									</p>
									<p className="text-gray-600 text-xs line-clamp-3 leading-relaxed">
										{event.description}
									</p>
								</div>
							))}
						</div>
					</Card>
				) : events && events.length > 0 ? (
					<Card title="Major Events" className="mb-8">
						<div className="py-8 text-center">
							<p className="mb-2 text-gray-500">
								No events match the selected filters
							</p>
							<button
								onClick={() => {
									setSelectedEventTypes([]);
									if (dateRange) {
										setStartDate(dateRange.min_date);
										setEndDate(dateRange.max_date);
									}
								}}
								className="font-medium text-blue-600 hover:text-blue-800 text-sm"
							>
								Reset filters
							</button>
						</div>
					</Card>
				) : null}

				{/* API Connection Error */}
				{!apiHealthy && apiHealthy !== null && (
					<ErrorDisplay
						error="Cannot connect to backend API. Make sure the Flask server is running on http://localhost:5000"
						onRetry={() => checkHealth().then(setApiHealthy)}
					/>
				)}
			</main>

			{/* Footer */}
			<footer className="bg-white mt-12 border-gray-200 border-t">
				<div className="mx-auto px-4 sm:px-6 lg:px-8 py-6 max-w-7xl">
					<p className="text-gray-600 text-sm text-center">
						Brent Oil Change Point Analysis Dashboard © 2026 |
						Birhan Energies
					</p>
				</div>
			</footer>
		</div>
	);
}

export default App;
