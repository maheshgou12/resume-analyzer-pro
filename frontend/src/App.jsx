import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import Login from "./pages/Login";
import Upload from "./pages/Upload";
import AdminDashboard from "./pages/AdminDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <nav className="navbar">
          <div className="brand">
            <span className="brand-icon">📄</span>
            Resume Analyzer <span>Pro</span>
          </div>

          <div className="nav-links">
            <Link to="/">Analyze</Link>
            <Link to="/login">Login</Link>
            <Link to="/admin">Admin Dashboard</Link>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Upload />} />
            <Route path="/login" element={<Login />} />
            <Route path="/admin" element={<AdminDashboard />} />
          </Routes>
        </main>

        <footer>
          Resume Analyzer Pro • AI-powered resume analysis
        </footer>
      </div>
    </BrowserRouter>
  );
}
