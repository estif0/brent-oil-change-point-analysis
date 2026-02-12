/**
 * Toggle Switch Component
 * 
 * Reusable toggle switch for boolean settings
 */

interface ToggleSwitchProps {
	enabled: boolean;
	onChange: (enabled: boolean) => void;
	label?: string;
	size?: 'sm' | 'md' | 'lg';
}

export function ToggleSwitch({ enabled, onChange, label, size = 'md' }: ToggleSwitchProps) {
	const sizes = {
		sm: { switch: 'w-8 h-4', circle: 'w-3 h-3', translate: 'translate-x-4' },
		md: { switch: 'w-11 h-6', circle: 'w-5 h-5', translate: 'translate-x-5' },
		lg: { switch: 'w-14 h-7', circle: 'w-6 h-6', translate: 'translate-x-7' },
	};

	const { switch: switchSize, circle: circleSize, translate } = sizes[size];

	return (
		<label className="flex items-center gap-3 cursor-pointer">
			{label && (
				<span className="text-sm font-medium text-gray-700">{label}</span>
			)}
			<div
				onClick={() => onChange(!enabled)}
				className={`relative inline-flex ${switchSize} items-center rounded-full transition-colors ${
					enabled ? 'bg-blue-600' : 'bg-gray-300'
				}`}
			>
				<span
					className={`${circleSize} inline-block transform rounded-full bg-white transition-transform ${
						enabled ? translate : 'translate-x-1'
					}`}
				/>
			</div>
		</label>
	);
}
