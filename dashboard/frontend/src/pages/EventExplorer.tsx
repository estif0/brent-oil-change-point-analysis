import React, { useState, useMemo } from "react";
import { ArrowLeft, Search, Calendar, Filter, X } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useEvents } from "../hooks/useData";
import { Card } from "../components/ui";
import { LoadingSpinner } from "../components/ui/LoadingSpinner";
import { ErrorDisplay } from "../components/ui/ErrorDisplay";
import { format, parseISO } from "date-fns";

const EVENT_TYPE_COLORS: Record<string, string> = {
	geopolitical: "bg-red-100 text-red-700 border-red-200",
	opec_decision: "bg-blue-100 text-blue-700 border-blue-200",
	economic_shock: "bg-amber-100 text-amber-700 border-amber-200",
	sanction: "bg-purple-100 text-purple-700 border-purple-200",
};

export const EventExplorer: React.FC = () => {
	const navigate = useNavigate();
	const { data: eventsData, loading, error } = useEvents();

	const [searchTerm, setSearchTerm] = useState("");
	const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
	const [sortBy, setSortBy] = useState<"date" | "name">("date");
	const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

	// Get unique event types
	const eventTypes = useMemo(() => {
		if (!eventsData?.events) return [];
		return Array.from(new Set(eventsData.events.map((e) => e.event_type)));
	}, [eventsData]);

	// Filter and sort events
	const filteredEvents = useMemo(() => {
		if (!eventsData?.events) return [];

		let filtered = eventsData.events;

		// Filter by search term
		if (searchTerm) {
			const search = searchTerm.toLowerCase();
			filtered = filtered.filter(
				(e) =>
					e.name.toLowerCase().includes(search) ||
					e.description.toLowerCase().includes(search),
			);
		}

		// Filter by event type
		if (selectedTypes.length > 0) {
			filtered = filtered.filter((e) =>
				selectedTypes.includes(e.event_type),
			);
		}

		// Sort
		filtered.sort((a, b) => {
			if (sortBy === "date") {
				const dateA = parseISO(a.date).getTime();
				const dateB = parseISO(b.date).getTime();
				return sortOrder === "asc" ? dateA - dateB : dateB - dateA;
			} else {
				return sortOrder === "asc"
					? a.name.localeCompare(b.name)
					: b.name.localeCompare(a.name);
			}
		});

		return filtered;
	}, [eventsData, searchTerm, selectedTypes, sortBy, sortOrder]);

	const toggleEventType = (type: string) => {
		setSelectedTypes((prev) =>
			prev.includes(type)
				? prev.filter((t) => t !== type)
				: [...prev, type],
		);
	};

	const clearFilters = () => {
		setSearchTerm("");
		setSelectedTypes([]);
	};

	if (loading) return <LoadingSpinner />;
	if (error) return <ErrorDisplay message={error} />;

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
								Event Explorer
							</h1>
							<p className="text-slate-600 text-sm">
								Browse and filter {eventsData?.count || 0}{" "}
								historical events affecting Brent oil prices
							</p>
						</div>
					</div>
				</div>
			</header>

			<main className="space-y-6 mx-auto px-4 py-8 max-w-7xl">
				{/* Filters */}
				<Card className="p-6">
					<div className="space-y-4">
						{/* Search Bar */}
						<div className="relative">
							<Search className="top-1/2 left-3 absolute w-5 h-5 text-slate-400 -translate-y-1/2 transform" />
							<input
								type="text"
								placeholder="Search events by name or description..."
								value={searchTerm}
								onChange={(e) => setSearchTerm(e.target.value)}
								className="py-3 pr-4 pl-10 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full"
							/>
						</div>

						{/* Filters Row */}
						<div className="flex flex-wrap items-center gap-4">
							{/* Event Type Filters */}
							<div className="flex items-center gap-2">
								<Filter className="w-4 h-4 text-slate-600" />
								<span className="font-medium text-slate-700 text-sm">
									Event Type:
								</span>
								{eventTypes.map((type) => (
									<button
										key={type}
										onClick={() => toggleEventType(type)}
										className={`px-3 py-1 text-sm rounded-full border transition-all ${
											selectedTypes.includes(type)
												? EVENT_TYPE_COLORS[type]
												: "bg-white text-slate-600 border-slate-300 hover:border-slate-400"
										}`}
									>
										{type.replace("_", " ")}
									</button>
								))}
							</div>

							{/* Sort Controls */}
							<div className="flex items-center gap-2 ml-auto">
								<span className="font-medium text-slate-700 text-sm">
									Sort by:
								</span>
								<select
									value={sortBy}
									onChange={(e) =>
										setSortBy(
											e.target.value as "date" | "name",
										)
									}
									className="px-3 py-1 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
								>
									<option value="date">Date</option>
									<option value="name">Name</option>
								</select>
								<button
									onClick={() =>
										setSortOrder((prev) =>
											prev === "asc" ? "desc" : "asc",
										)
									}
									className="hover:bg-slate-50 px-3 py-1 border border-slate-300 rounded-lg text-sm transition-colors"
								>
									{sortOrder === "asc" ? "↑ Asc" : "↓ Desc"}
								</button>
							</div>

							{/* Clear Filters */}
							{(searchTerm || selectedTypes.length > 0) && (
								<button
									onClick={clearFilters}
									className="flex items-center gap-1 hover:bg-red-50 px-3 py-1 rounded-lg text-red-600 text-sm transition-colors"
								>
									<X className="w-4 h-4" />
									Clear Filters
								</button>
							)}
						</div>
					</div>
				</Card>

				{/* Results Count */}
				<div className="flex justify-between items-center">
					<p className="text-slate-600 text-sm">
						Showing <strong>{filteredEvents.length}</strong> of{" "}
						<strong>{eventsData?.count}</strong> events
					</p>
				</div>

				{/* Events Grid */}
				{filteredEvents.length === 0 ? (
					<Card className="p-12 text-center">
						<div className="mb-2 text-slate-400">
							<Search className="mx-auto mb-4 w-12 h-12" />
						</div>
						<h3 className="mb-2 font-semibold text-slate-900 text-lg">
							No events found
						</h3>
						<p className="text-slate-600">
							Try adjusting your search or filters
						</p>
					</Card>
				) : (
					<div className="gap-4 grid grid-cols-1 md:grid-cols-2">
						{filteredEvents.map((event) => (
							<Card
								key={event.id}
								className="group hover:shadow-lg p-6 transition-shadow cursor-pointer"
							>
								<div className="flex justify-between items-start mb-3">
									<h3 className="font-semibold text-slate-900 group-hover:text-blue-600 transition-colors">
										{event.name}
									</h3>
									<span
										className={`text-xs px-2 py-1 rounded-full border ${
											EVENT_TYPE_COLORS[event.event_type]
										}`}
									>
										{event.event_type.replace("_", " ")}
									</span>
								</div>

								<p className="mb-4 text-slate-600 text-sm line-clamp-3">
									{event.description}
								</p>

								<div className="flex justify-between items-center pt-3 border-slate-100 border-t text-slate-500 text-xs">
									<span className="flex items-center gap-1">
										<Calendar className="w-3 h-3" />
										{format(
											parseISO(event.date),
											"MMM dd, yyyy",
										)}
									</span>
									<span className="font-medium text-slate-700">
										Impact: {event.expected_impact}
									</span>
								</div>
							</Card>
						))}
					</div>
				)}
			</main>
		</div>
	);
};
