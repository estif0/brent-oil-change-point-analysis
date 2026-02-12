/**
 * Main App Component
 *
 * Brent Oil Change Point Analysis Dashboard
 */

import { useEffect, useState } from "react";
import { Activity, TrendingUp, Calendar, AlertTriangle } from "lucide-react";
import { LoadingSpinner, ErrorDisplay, Card, ToggleSwitch } from "./components/ui";
import { PriceChart } from "./components/charts";
import { useChangePoints, useEvents, useDateRange, usePrices } from "./hooks/useData";
import { checkHealth } from "./lib/api-client";

function App() {
	const [apiHealthy, setApiHealthy] = useState<boolean | null>(null);
	const [showChangePoints, setShowChangePoints] = useState(true);
	const [showEvents, setShowEvents] = useState(true);
	const [showAllEvents, setShowAllEvents] = useState(false);

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
	} = usePrices();

	// Check API health on mount
	useEffect(() => {
		checkHealth().then(setApiHealthy);
	}, []);

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
							<div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
								<p className="text-gray-600 text-sm">
									Historical Brent crude oil prices from {dateRange?.min_date} to{" "}
									{dateRange?.max_date}
								</p>
								<div className="flex gap-4">
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
							<PriceChart
								data={prices}
								changePoints={changePoints || []}
								events={events || []}
								showChangePoints={showChangePoints}
								showEvents={showEvents}
								height={450}
							/>
						</>
					) : (
						<p className="text-center text-gray-500 py-8">
							No price data available
						</p>
					)}
				</Card>

				{/* Change Points Section */}
				{changePoints && changePoints.length > 0 && (
					<Card title="Detected Change Points" className="mb-8">
						<div className="space-y-4">
							{changePoints.map((cp) => (
								<div
									key={cp.id}
									className="hover:shadow-md p-4 border border-gray-200 rounded-lg transition-shadow"
								>
									<div className="flex justify-between items-start">
										<div className="flex-1">
											<div className="flex items-center gap-2 mb-2">
												<h3 className="font-semibold text-gray-900 text-lg">
													{cp.date}
												</h3>
												<span className="bg-blue-100 px-2 py-1 rounded font-medium text-blue-800 text-xs">
													{(
														cp.confidence * 100
													).toFixed(0)}
													% confidence
												</span>
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
				{events && events.length > 0 && (
					<Card title="Major Events" className="mb-8">
						<p className="text-gray-600 text-sm mb-4">
							Historical events that may have influenced Brent oil prices. 
							Includes geopolitical events, OPEC decisions, economic shocks, and sanctions.
						</p>
						<div className="gap-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
							{(showAllEvents ? events : events.slice(0, 6)).map((event) => (
								<div
									key={event.id}
									className="hover:shadow-md hover:border-gray-300 p-4 border border-gray-200 rounded-lg transition-all cursor-pointer"
								>
									<div className="flex justify-between items-start mb-2">
										<h4 className="font-semibold text-gray-900 text-sm">
											{event.event_name}
										</h4>
										<span
											className={`px-2 py-1 text-xs font-medium rounded shrink-0 ml-2 ${
												event.event_type ===
												"geopolitical"
													? "bg-red-100 text-red-800"
													: event.event_type ===
														  "economic_shock"
														? "bg-amber-100 text-amber-800"
														: event.event_type ===
															  "opec_decision"
															? "bg-green-100 text-green-800"
															: "bg-purple-100 text-purple-800"
											}`}
										>
											{event.event_type.replace('_', ' ')}
										</span>
									</div>
									<p className="mb-2 text-gray-600 text-xs font-medium">
										{event.date}
									</p>
									<p className="text-gray-500 text-xs line-clamp-3">
										{event.description}
									</p>
								</div>
							))}
						</div>
						{events.length > 6 && (
							<div className="mt-6 text-center">
								<button
									onClick={() => setShowAllEvents(!showAllEvents)}
									className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium text-sm"
								>
									{showAllEvents ? 'Show Less' : `Show All ${events.length} Events`}
								</button>
							</div>
						)}
					</Card>
				)}

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
