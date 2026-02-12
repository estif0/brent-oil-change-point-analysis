import React, { useState, useMemo } from "react";
import {
	ArrowLeft,
	TrendingUp,
	TrendingDown,
	Calendar,
	Percent,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { usePrices, useChangePoints, useEvents } from "../hooks/useData";
import { Card } from "../components/ui";
import { LoadingSpinner } from "../components/ui/LoadingSpinner";
import { ErrorDisplay } from "../components/ui/ErrorDisplay";
import { PriceChart } from "../components/charts/PriceChart";
import { format, parseISO, subDays, addDays } from "date-fns";

export const DetailedAnalysis: React.FC = () => {
	const navigate = useNavigate();
	const {
		data: changePointsData,
		loading: cpLoading,
		error: cpError,
	} = useChangePoints();
	const {
		data: eventsData,
		loading: eventsLoading,
		error: eventsError,
	} = useEvents();
	const [selectedChangePoint, setSelectedChangePoint] = useState<
		string | null
	>(null);

	// Get selected change point details
	const selectedCP = useMemo(() => {
		if (!changePointsData?.changepoints || !selectedChangePoint)
			return null;
		return changePointsData.changepoints.find(
			(cp) => cp.date === selectedChangePoint,
		);
	}, [changePointsData, selectedChangePoint]);

	// Fetch prices around the selected change point
	const analysisWindow = 90; // days before and after
	const startDate = selectedCP
		? format(
				subDays(parseISO(selectedCP.date), analysisWindow),
				"yyyy-MM-dd",
			)
		: undefined;
	const endDate = selectedCP
		? format(
				addDays(parseISO(selectedCP.date), analysisWindow),
				"yyyy-MM-dd",
			)
		: undefined;

	const { data: pricesData, loading: pricesLoading } = usePrices(
		startDate,
		endDate,
	);

	// Calculate statistics
	const stats = useMemo(() => {
		if (!pricesData?.prices || !selectedCP) return null;

		const cpDate = parseISO(selectedCP.date);
		const beforePrices = pricesData.prices
			.filter((p) => parseISO(p.date) < cpDate)
			.map((p) => p.price);
		const afterPrices = pricesData.prices
			.filter((p) => parseISO(p.date) >= cpDate)
			.map((p) => p.price);

		const avgBefore =
			beforePrices.reduce((a, b) => a + b, 0) / beforePrices.length;
		const avgAfter =
			afterPrices.reduce((a, b) => a + b, 0) / afterPrices.length;
		const change = avgAfter - avgBefore;
		const changePercent = (change / avgBefore) * 100;

		return {
			avgBefore: avgBefore.toFixed(2),
			avgAfter: avgAfter.toFixed(2),
			change: change.toFixed(2),
			changePercent: changePercent.toFixed(2),
			beforeCount: beforePrices.length,
			afterCount: afterPrices.length,
		};
	}, [pricesData, selectedCP]);

	// Find related events
	const relatedEvents = useMemo(() => {
		if (!eventsData?.events || !selectedCP) return [];
		const cpDate = parseISO(selectedCP.date);
		return eventsData.events.filter((event) => {
			const eventDate = parseISO(event.date);
			const daysDiff = Math.abs(
				(eventDate.getTime() - cpDate.getTime()) /
					(1000 * 60 * 60 * 24),
			);
			return daysDiff <= 60; // Within 60 days
		});
	}, [eventsData, selectedCP]);

	if (cpLoading || eventsLoading) return <LoadingSpinner />;
	if (cpError) return <ErrorDisplay message={cpError} />;

	return (
		<div className="bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100 min-h-screen">
			{/* Header */}
			<header className="top-0 z-10 sticky bg-white/80 backdrop-blur-sm border-slate-200 border-b">
				<div className="mx-auto px-4 py-4 max-w-7xl">
					<div className="flex items-center gap-4">
						<button
							onClick={() => navigate("/")}
							className="hover:bg-slate-100 p-2 rounded-lg transition-colors"
						>
							<ArrowLeft className="w-5 h-5" />
						</button>
						<div>
							<h1 className="font-bold text-slate-900 text-2xl">
								Detailed Change Point Analysis
							</h1>
							<p className="text-slate-600 text-sm">
								Deep dive into detected change points and their
								impacts
							</p>
						</div>
					</div>
				</div>
			</header>

			<main className="space-y-6 mx-auto px-4 py-8 max-w-7xl">
				{/* Change Point Selector */}
				<Card className="p-6">
					<h2 className="mb-4 font-semibold text-lg">
						Select a Change Point to Analyze
					</h2>
					<div className="gap-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
						{changePointsData?.changepoints.map((cp) => (
							<button
								key={cp.date}
								onClick={() => setSelectedChangePoint(cp.date)}
								className={`p-4 rounded-lg border-2 transition-all text-left ${
									selectedChangePoint === cp.date
										? "border-blue-500 bg-blue-50"
										: "border-slate-200 hover:border-blue-300 bg-white"
								}`}
							>
								<div className="flex items-center gap-2 mb-2">
									<Calendar className="w-4 h-4 text-blue-600" />
									<span className="font-semibold">
										{format(
											parseISO(cp.date),
											"MMM dd, yyyy",
										)}
									</span>
								</div>
								<div className="text-slate-600 text-sm">
									Confidence:{" "}
									<span className="font-medium text-slate-900">
										{cp.confidence}%
									</span>
								</div>
							</button>
						))}
					</div>
				</Card>

				{/* Analysis Results */}
				{selectedCP && (
					<>
						{/* Statistics Cards */}
						<div className="gap-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
							<Card className="bg-gradient-to-br from-blue-500 to-blue-600 p-6 text-white">
								<div className="flex justify-between items-center mb-2">
									<span className="opacity-90 font-medium text-sm">
										Avg Before
									</span>
									<TrendingDown className="opacity-75 w-5 h-5" />
								</div>
								<div className="font-bold text-3xl">
									${stats?.avgBefore}
								</div>
								<div className="opacity-75 mt-1 text-xs">
									{stats?.beforeCount} data points
								</div>
							</Card>

							<Card className="bg-gradient-to-br from-green-500 to-green-600 p-6 text-white">
								<div className="flex justify-between items-center mb-2">
									<span className="opacity-90 font-medium text-sm">
										Avg After
									</span>
									<TrendingUp className="opacity-75 w-5 h-5" />
								</div>
								<div className="font-bold text-3xl">
									${stats?.avgAfter}
								</div>
								<div className="opacity-75 mt-1 text-xs">
									{stats?.afterCount} data points
								</div>
							</Card>

							<Card className="bg-gradient-to-br from-purple-500 to-purple-600 p-6 text-white">
								<div className="flex justify-between items-center mb-2">
									<span className="opacity-90 font-medium text-sm">
										Price Change
									</span>
									<Percent className="opacity-75 w-5 h-5" />
								</div>
								<div className="font-bold text-3xl">
									${stats?.change}
								</div>
								<div className="opacity-75 mt-1 text-xs">
									Absolute difference
								</div>
							</Card>

							<Card
								className={`p-6 bg-gradient-to-br ${
									parseFloat(stats?.changePercent || "0") >= 0
										? "from-emerald-500 to-emerald-600"
										: "from-red-500 to-red-600"
								} text-white`}
							>
								<div className="flex justify-between items-center mb-2">
									<span className="opacity-90 font-medium text-sm">
										% Change
									</span>
									{parseFloat(stats?.changePercent || "0") >=
									0 ? (
										<TrendingUp className="opacity-75 w-5 h-5" />
									) : (
										<TrendingDown className="opacity-75 w-5 h-5" />
									)}
								</div>
								<div className="font-bold text-3xl">
									{stats?.changePercent}%
								</div>
								<div className="opacity-75 mt-1 text-xs">
									Percentage change
								</div>
							</Card>
						</div>

						{/* Price Chart */}
						<Card className="p-6">
							<h2 className="mb-4 font-semibold text-lg">
								Price Trend Around Change Point (
								{analysisWindow} days window)
							</h2>
							{pricesLoading ? (
								<LoadingSpinner />
							) : pricesData?.prices ? (
								<PriceChart
									data={pricesData.prices}
									changePoints={[selectedCP]}
									events={relatedEvents}
									showChangePoints={true}
									showEvents={true}
								/>
							) : (
								<p className="text-slate-600">
									No data available
								</p>
							)}
						</Card>

						{/* Related Events */}
						{relatedEvents.length > 0 && (
							<Card className="p-6">
								<h2 className="mb-4 font-semibold text-lg">
									Related Events (within 60 days)
								</h2>
								<div className="space-y-4">
									{relatedEvents.map((event) => (
										<div
											key={event.id}
											className="bg-slate-50 p-4 border border-slate-200 rounded-lg"
										>
											<div className="flex justify-between items-start mb-2">
												<h3 className="font-semibold text-slate-900">
													{event.name}
												</h3>
												<span className="bg-blue-100 px-2 py-1 rounded-full text-blue-700 text-xs">
													{event.event_type}
												</span>
											</div>
											<p className="mb-2 text-slate-600 text-sm">
												{event.description}
											</p>
											<div className="flex items-center gap-4 text-slate-500 text-xs">
												<span className="flex items-center gap-1">
													<Calendar className="w-3 h-3" />
													{format(
														parseISO(event.date),
														"MMM dd, yyyy",
													)}
												</span>
												<span>
													Expected Impact:{" "}
													{event.expected_impact}
												</span>
											</div>
										</div>
									))}
								</div>
							</Card>
						)}

						{/* Impact Statement */}
						<Card className="bg-gradient-to-br from-slate-800 to-slate-900 p-6 text-white">
							<h2 className="mb-4 font-semibold text-lg">
								Impact Statement
							</h2>
							<p className="text-lg leading-relaxed">
								On{" "}
								<strong>
									{format(
										parseISO(selectedCP.date),
										"MMMM dd, yyyy",
									)}
								</strong>
								, a significant change point was detected with{" "}
								<strong>
									{selectedCP.confidence}% confidence
								</strong>
								. The average daily Brent oil price shifted from{" "}
								<strong>${stats?.avgBefore}</strong> to{" "}
								<strong>${stats?.avgAfter}</strong>,
								representing a change of{" "}
								<strong>${stats?.change}</strong> or{" "}
								<strong>{stats?.changePercent}%</strong>.
								{relatedEvents.length > 0 && (
									<>
										{" "}
										This change point coincides with{" "}
										{relatedEvents.length} major event(s),
										suggesting a potential causal
										relationship.
									</>
								)}
							</p>
						</Card>
					</>
				)}
			</main>
		</div>
	);
};
