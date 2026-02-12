/**
 * Filter Dropdown Component
 *
 * Multi-select dropdown for filtering by event types
 */

import { Filter } from "lucide-react";

interface FilterDropdownProps {
	label: string;
	options: string[];
	selectedOptions: string[];
	onToggle: (option: string) => void;
	onReset: () => void;
	className?: string;
}

export function FilterDropdown({
	label,
	options,
	selectedOptions,
	onToggle,
	onReset,
	className = "",
}: FilterDropdownProps) {
	return (
		<div className={`flex flex-col gap-2 ${className}`}>
			<div className="flex justify-between items-center">
				<label className="flex items-center gap-2 font-medium text-gray-700 text-sm">
					<Filter className="w-4 h-4" />
					{label}
				</label>
				{selectedOptions.length > 0 && (
					<button
						onClick={onReset}
						className="text-blue-600 hover:text-blue-800 text-xs"
					>
						Reset
					</button>
				)}
			</div>
			<div className="flex flex-wrap gap-2">
				{options.map((option) => {
					const isSelected = selectedOptions.includes(option);
					return (
						<button
							key={option}
							onClick={() => onToggle(option)}
							className={`px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${
								isSelected
									? "bg-blue-600 text-white border-blue-600"
									: "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
							}`}
						>
							{option}
						</button>
					);
				})}
			</div>
		</div>
	);
}
