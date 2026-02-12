import React from "react";
import {
	ArrowLeft,
	BarChart3,
	Brain,
	TrendingUp,
	Database,
	Code2,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Card } from "../components/ui";

export const About: React.FC = () => {
	const navigate = useNavigate();

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
								About This Project
							</h1>
							<p className="text-slate-600 text-sm">
								Methodology, technologies, and background
							</p>
						</div>
					</div>
				</div>
			</header>

			<main className="space-y-6 mx-auto px-4 py-8 max-w-5xl">
				{/* Project Overview */}
				<Card className="bg-gradient-to-br from-blue-600 to-blue-700 p-8 text-white">
					<div className="flex items-start gap-4 mb-4">
						<div className="bg-white/20 p-3 rounded-lg">
							<BarChart3 className="w-8 h-8" />
						</div>
						<div>
							<h2 className="mb-2 font-bold text-2xl">
								Brent Oil Change Point Analysis
							</h2>
							<p className="text-blue-100 leading-relaxed">
								A data-driven analysis platform that uses
								Bayesian change point detection to identify and
								quantify how major geopolitical events, OPEC
								decisions, and economic shocks impact Brent oil
								prices.
							</p>
						</div>
					</div>
					<div className="gap-4 grid grid-cols-1 md:grid-cols-3 mt-6">
						<div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
							<div className="mb-1 font-bold text-3xl">35+</div>
							<div className="text-blue-100 text-sm">
								Years of Data
							</div>
						</div>
						<div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
							<div className="mb-1 font-bold text-3xl">9,154</div>
							<div className="text-blue-100 text-sm">
								Price Records
							</div>
						</div>
						<div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
							<div className="mb-1 font-bold text-3xl">17</div>
							<div className="text-blue-100 text-sm">
								Major Events
							</div>
						</div>
					</div>
				</Card>

				{/* Business Context */}
				<Card className="p-8">
					<h2 className="mb-4 font-bold text-slate-900 text-xl">
						Business Context
					</h2>
					<p className="mb-4 text-slate-700 leading-relaxed">
						This project serves <strong>Birhan Energies</strong>, a
						consultancy firm providing data-driven insights to
						energy sector stakeholders. The analysis helps guide
						investment strategies, policy development, and
						operational planning by understanding how external
						factors influence oil prices.
					</p>
					<div className="gap-4 grid grid-cols-1 md:grid-cols-2 mt-6">
						<div className="bg-blue-50 p-4 border border-blue-200 rounded-lg">
							<h3 className="mb-2 font-semibold text-blue-900">
								Target Audience
							</h3>
							<ul className="space-y-1 text-blue-700 text-sm">
								<li>• Energy investors and traders</li>
								<li>• Policy makers and regulators</li>
								<li>• Oil & gas companies</li>
								<li>• Economic analysts</li>
							</ul>
						</div>
						<div className="bg-green-50 p-4 border border-green-200 rounded-lg">
							<h3 className="mb-2 font-semibold text-green-900">
								Key Insights
							</h3>
							<ul className="space-y-1 text-green-700 text-sm">
								<li>• Price change point detection</li>
								<li>• Event-price correlation analysis</li>
								<li>• Quantitative impact assessment</li>
								<li>• Historical trend patterns</li>
							</ul>
						</div>
					</div>
				</Card>

				{/* Methodology */}
				<Card className="p-8">
					<div className="flex items-center gap-3 mb-4">
						<Brain className="w-6 h-6 text-purple-600" />
						<h2 className="font-bold text-slate-900 text-xl">
							Methodology
						</h2>
					</div>

					<div className="space-y-6">
						<div>
							<h3 className="mb-2 font-semibold text-slate-900">
								1. Bayesian Change Point Detection
							</h3>
							<p className="text-slate-700 text-sm leading-relaxed">
								We use PyMC to build a Bayesian change point
								model that identifies significant structural
								breaks in the Brent oil price time series. The
								model estimates the probability distribution of
								change point locations (τ) and quantifies the
								confidence level of each detection.
							</p>
							<div className="bg-slate-50 mt-3 p-3 border border-slate-200 rounded font-mono text-xs">
								<div>prior: τ ~ DiscreteUniform(0, T)</div>
								<div>μ₁, μ₂ ~ Normal(μ_prior, σ_prior)</div>
								<div>likelihood: y ~ Normal(μ(t), σ)</div>
							</div>
						</div>

						<div>
							<h3 className="mb-2 font-semibold text-slate-900">
								2. Event Association
							</h3>
							<p className="text-slate-700 text-sm leading-relaxed">
								Detected change points are matched with
								historical events (geopolitical conflicts, OPEC
								decisions, economic shocks, sanctions) within a
								temporal window. This helps identify potential
								causal relationships between external factors
								and price movements.
							</p>
						</div>

						<div>
							<h3 className="mb-2 font-semibold text-slate-900">
								3. Impact Quantification
							</h3>
							<p className="text-slate-700 text-sm leading-relaxed">
								For each change point, we calculate before/after
								statistics including average prices, volatility,
								and percentage changes. This provides
								quantitative impact statements that can guide
								decision-making.
							</p>
						</div>

						<div>
							<h3 className="mb-2 font-semibold text-slate-900">
								4. Statistical Validation
							</h3>
							<p className="text-slate-700 text-sm leading-relaxed">
								We perform stationarity tests (Augmented
								Dickey-Fuller, KPSS) and analyze convergence
								diagnostics (R-hat values, trace plots) to
								ensure model reliability and statistical
								validity.
							</p>
						</div>
					</div>
				</Card>

				{/* Data Sources */}
				<Card className="p-8">
					<div className="flex items-center gap-3 mb-4">
						<Database className="w-6 h-6 text-blue-600" />
						<h2 className="font-bold text-slate-900 text-xl">
							Data Sources
						</h2>
					</div>

					<div className="space-y-4">
						<div className="bg-slate-50 p-4 border border-slate-200 rounded-lg">
							<div className="flex justify-between items-center mb-2">
								<h3 className="font-semibold text-slate-900">
									Brent Oil Price Data
								</h3>
								<span className="bg-blue-100 px-2 py-1 rounded-full text-blue-700 text-xs">
									Daily
								</span>
							</div>
							<p className="mb-2 text-slate-600 text-sm">
								Historical daily Brent crude oil prices from May
								20, 1987 to September 30, 2022
							</p>
							<div className="text-slate-500 text-xs">
								Source: Energy markets data
							</div>
						</div>

						<div className="bg-slate-50 p-4 border border-slate-200 rounded-lg">
							<div className="flex justify-between items-center mb-2">
								<h3 className="font-semibold text-slate-900">
									Historical Events
								</h3>
								<span className="bg-green-100 px-2 py-1 rounded-full text-green-700 text-xs">
									Curated
								</span>
							</div>
							<p className="mb-2 text-slate-600 text-sm">
								17 major geopolitical events, OPEC decisions,
								economic shocks, and sanctions
							</p>
							<div className="text-slate-500 text-xs">
								Categories: Geopolitical, OPEC, Economic,
								Sanctions
							</div>
						</div>
					</div>
				</Card>

				{/* Technology Stack */}
				<Card className="p-8">
					<div className="flex items-center gap-3 mb-4">
						<Code2 className="w-6 h-6 text-emerald-600" />
						<h2 className="font-bold text-slate-900 text-xl">
							Technology Stack
						</h2>
					</div>

					<div className="gap-6 grid grid-cols-1 md:grid-cols-2">
						<div>
							<h3 className="mb-3 font-semibold text-slate-900">
								Data Analysis
							</h3>
							<ul className="space-y-2 text-slate-700 text-sm">
								<li className="flex items-center gap-2">
									<div className="bg-blue-500 rounded-full w-2 h-2"></div>
									<strong>Python 3.x</strong> - Core
									programming language
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-blue-500 rounded-full w-2 h-2"></div>
									<strong>PyMC</strong> - Bayesian modeling
									and MCMC sampling
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-blue-500 rounded-full w-2 h-2"></div>
									<strong>pandas</strong> - Data manipulation
									and analysis
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-blue-500 rounded-full w-2 h-2"></div>
									<strong>matplotlib & seaborn</strong> - Data
									visualization
								</li>
							</ul>
						</div>

						<div>
							<h3 className="mb-3 font-semibold text-slate-900">
								Backend
							</h3>
							<ul className="space-y-2 text-slate-700 text-sm">
								<li className="flex items-center gap-2">
									<div className="bg-green-500 rounded-full w-2 h-2"></div>
									<strong>Flask</strong> - REST API framework
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-green-500 rounded-full w-2 h-2"></div>
									<strong>Flask-RESTful</strong> - API
									resource management
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-green-500 rounded-full w-2 h-2"></div>
									<strong>Flask-CORS</strong> - Cross-origin
									requests
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-green-500 rounded-full w-2 h-2"></div>
									<strong>Swagger UI</strong> - API
									documentation
								</li>
							</ul>
						</div>

						<div>
							<h3 className="mb-3 font-semibold text-slate-900">
								Frontend
							</h3>
							<ul className="space-y-2 text-slate-700 text-sm">
								<li className="flex items-center gap-2">
									<div className="bg-purple-500 rounded-full w-2 h-2"></div>
									<strong>React 19</strong> - UI framework
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-purple-500 rounded-full w-2 h-2"></div>
									<strong>TypeScript</strong> - Type-safe
									development
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-purple-500 rounded-full w-2 h-2"></div>
									<strong>Vite</strong> - Build tool and dev
									server
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-purple-500 rounded-full w-2 h-2"></div>
									<strong>Tailwind CSS</strong> - Styling
									framework
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-purple-500 rounded-full w-2 h-2"></div>
									<strong>Recharts</strong> - Data
									visualization
								</li>
							</ul>
						</div>

						<div>
							<h3 className="mb-3 font-semibold text-slate-900">
								Development Tools
							</h3>
							<ul className="space-y-2 text-slate-700 text-sm">
								<li className="flex items-center gap-2">
									<div className="bg-amber-500 rounded-full w-2 h-2"></div>
									<strong>pytest</strong> - Python testing
									framework
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-amber-500 rounded-full w-2 h-2"></div>
									<strong>Git</strong> - Version control
								</li>
								<li className="flex items-center gap-2">
									<div className="bg-amber-500 rounded-full w-2 h-2"></div>
									<strong>pnpm</strong> - Package manager
								</li>
							</ul>
						</div>
					</div>
				</Card>

				{/* Assumptions & Limitations */}
				<Card className="bg-amber-50 p-8 border-amber-200">
					<h2 className="mb-4 font-bold text-slate-900 text-xl">
						Assumptions & Limitations
					</h2>
					<div className="space-y-3 text-slate-700 text-sm">
						<p>
							<strong>Correlation vs Causation:</strong> This
							analysis identifies temporal correlations between
							events and price changes but does not establish
							definitive causal relationships.
						</p>
						<p>
							<strong>Data Quality:</strong> Results depend on the
							accuracy and completeness of historical price data
							and event records.
						</p>
						<p>
							<strong>Model Simplicity:</strong> The single change
							point model may not capture all market dynamics.
							Multiple factors often influence prices
							simultaneously.
						</p>
						<p>
							<strong>Temporal Window:</strong> Event association
							uses a fixed temporal window which may miss delayed
							impacts or anticipatory market movements.
						</p>
					</div>
				</Card>

				{/* Footer */}
				<div className="py-8 text-slate-600 text-sm text-center">
					<p>
						Developed for Birhan Energies • Data Analysis &
						Visualization Dashboard
					</p>
					<p className="mt-2">
						© 2026 Brent Oil Change Point Analysis Project
					</p>
				</div>
			</main>
		</div>
	);
};
