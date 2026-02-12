/**
 * Price Chart Component
 * 
 * Interactive time series chart displaying Brent oil prices with change points and events
 */

import { useMemo } from 'react';
import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	ResponsiveContainer,
	ReferenceLine,
	Legend,
} from 'recharts';
import type { PriceRecord, ChangePoint, Event } from '../../types';
import { format, parseISO } from 'date-fns';

interface PriceChartProps {
	data: PriceRecord[];
	changePoints?: ChangePoint[];
	events?: Event[];
	showChangePoints?: boolean;
	showEvents?: boolean;
	height?: number;
}

export function PriceChart({
	data,
	changePoints = [],
	events = [],
	showChangePoints = true,
	showEvents = true,
	height = 400,
}: PriceChartProps) {
	// Prepare chart data
	const chartData = useMemo(() => {
		return data.map((record) => ({
			date: record.date,
			price: record.price,
			timestamp: new Date(record.date).getTime(),
		}));
	}, [data]);

	// Custom tooltip
	const CustomTooltip = ({ active, payload }: any) => {
		if (active && payload && payload.length) {
			const data = payload[0].payload;
			return (
				<div className="bg-white p-3 border border-gray-200 shadow-lg rounded-lg">
					<p className="text-sm font-semibold text-gray-900">
						{format(parseISO(data.date), 'MMM dd, yyyy')}
					</p>
					<p className="text-sm text-gray-600">
						Price: <span className="font-bold text-blue-600">${data.price.toFixed(2)}</span>
					</p>
				</div>
			);
		}
		return null;
	};

	// Format date for x-axis
	const formatXAxis = (dateStr: string) => {
		try {
			return format(parseISO(dateStr), 'yyyy');
		} catch {
			return dateStr;
		}
	};

	return (
		<div className="w-full">
			<ResponsiveContainer width="100%" height={height}>
				<LineChart
					data={chartData}
					margin={{ top: 10, right: 30, left: 10, bottom: 10 }}
				>
					<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
					<XAxis
						dataKey="date"
						tickFormatter={formatXAxis}
						stroke="#6b7280"
						tick={{ fontSize: 12 }}
						minTickGap={50}
					/>
					<YAxis
						stroke="#6b7280"
						tick={{ fontSize: 12 }}
						label={{
							value: 'Price (USD)',
							angle: -90,
							position: 'insideLeft',
							style: { fontSize: 12, fill: '#6b7280' },
						}}
					/>
					<Tooltip content={<CustomTooltip />} />
					<Legend
						wrapperStyle={{ fontSize: 12, paddingTop: 10 }}
						iconType="line"
					/>

					{/* Main price line */}
					<Line
						type="monotone"
						dataKey="price"
						stroke="#2563eb"
						strokeWidth={2}
						dot={false}
						name="Brent Oil Price"
						isAnimationActive={false}
					/>

					{/* Change point markers */}
					{showChangePoints &&
						changePoints.map((cp) => (
							<ReferenceLine
								key={cp.id}
								x={cp.date}
								stroke="#dc2626"
								strokeWidth={2}
								strokeDasharray="3 3"
								label={{
									value: 'Change Point',
									position: 'top',
									fill: '#dc2626',
									fontSize: 10,
								}}
							/>
						))}

					{/* Event markers */}
					{showEvents &&
						events.slice(0, 10).map((event) => (
							<ReferenceLine
								key={event.id}
								x={event.date}
								stroke="#f59e0b"
								strokeWidth={1}
								strokeDasharray="2 2"
								label={{
									value: '▼',
									position: 'top',
									fill: '#f59e0b',
									fontSize: 12,
								}}
							/>
						))}
				</LineChart>
			</ResponsiveContainer>

			{/* Legend for markers */}
			<div className="flex items-center justify-center gap-6 mt-4 text-xs">
				{showChangePoints && changePoints.length > 0 && (
					<div className="flex items-center gap-2">
						<div className="w-8 h-0.5 bg-red-600 border-dashed border-t-2 border-red-600"></div>
						<span className="text-gray-600">Change Points ({changePoints.length})</span>
					</div>
				)}
				{showEvents && events.length > 0 && (
					<div className="flex items-center gap-2">
						<div className="w-8 h-0.5 bg-amber-500 border-dashed border-t border-amber-500"></div>
						<span className="text-gray-600">Events (showing 10 of {events.length})</span>
					</div>
				)}
			</div>
		</div>
	);
}
