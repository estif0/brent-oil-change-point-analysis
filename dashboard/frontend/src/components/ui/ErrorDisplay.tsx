/**
 * ErrorDisplay Component
 *
 * Display error messages with retry option
 */

import { AlertCircle } from "lucide-react";

interface ErrorDisplayProps {
	error: string;
	onRetry?: () => void;
	className?: string;
}

export function ErrorDisplay({
	error,
	onRetry,
	className = "",
}: ErrorDisplayProps) {
	return (
		<div
			className={`bg-red-50 border border-red-200 rounded-lg p-4 ${className}`}
		>
			<div className="flex items-start gap-3">
				<AlertCircle className="flex-shrink-0 mt-0.5 w-5 h-5 text-red-600" />
				<div className="flex-1">
					<h3 className="mb-1 font-semibold text-red-900 text-sm">
						Error
					</h3>
					<p className="text-red-700 text-sm">{error}</p>
					{onRetry && (
						<button
							onClick={onRetry}
							className="mt-3 font-medium text-red-600 hover:text-red-800 text-sm underline"
						>
							Try again
						</button>
					)}
				</div>
			</div>
		</div>
	);
}
