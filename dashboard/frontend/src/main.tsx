import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App.tsx";
import { DetailedAnalysis } from "./pages/DetailedAnalysis";
import { EventExplorer } from "./pages/EventExplorer";
import { About } from "./pages/About";

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<App />} />
				<Route path="/analysis" element={<DetailedAnalysis />} />
				<Route path="/events" element={<EventExplorer />} />
				<Route path="/about" element={<About />} />
			</Routes>
		</BrowserRouter>
	</StrictMode>,
);
