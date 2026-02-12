/**
 * Date Range Picker Component
 *
 * Allows users to select start and end dates for filtering data
 */

import { Calendar } from "lucide-react";
import type { DateRange } from "../../types";

interface DateRangePickerProps {
	startDate: string;
	endDate: string;
	onStartDateChange: (date: string) => void;
	onEndDateChange: (date: string) => void;
	availableRange?: DateRange;
	className?: string;
}

export function DateRangePicker({
	startDate,
	endDate,
	onStartDateChange,
	onEndDateChange,
	availableRange,
	className = "",
}: DateRangePickerProps) {
	return (
		<div className={`flex items-center gap-4 ${className}`}>
			<div className="flex items-center gap-2">
				<Calendar className="w-4 h-4 text-gray-500" />
				<span className="font-medium text-gray-700 text-sm">From:</span>
				<input
					type="date"
					value={startDate}
					onChange={(e) => onStartDateChange(e.target.value)}
					min={availableRange?.min_date}
					max={endDate || availableRange?.max_date}
					className="px-3 py-1.5 border border-gray-300 focus:border-blue-500 rounded-md focus:ring-2 focus:ring-blue-500 text-sm"
				/>
			</div>
			<div className="flex items-center gap-2">
				<span className="font-medium text-gray-700 text-sm">To:</span>
				<input
					type="date"
					value={endDate}
					onChange={(e) => onEndDateChange(e.target.value)}
					min={startDate || availableRange?.min_date}
					max={availableRange?.max_date}
					className="px-3 py-1.5 border border-gray-300 focus:border-blue-500 rounded-md focus:ring-2 focus:ring-blue-500 text-sm"
				/>
			</div>
		</div>
	);
}
