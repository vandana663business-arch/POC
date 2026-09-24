import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import SubProcessDetail from "./pages/SubProcessDetail";
import AlertsPage from "./pages/AlertsPage";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        Intake Staffing
        <span>Forecasting POC</span>
      </div>
      <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
        Overview
      </NavLink>
      <NavLink to="/alerts" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
        Alerts
      </NavLink>
    </aside>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/subprocess/:id" element={<SubProcessDetail />} />
            <Route path="/alerts" element={<AlertsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
