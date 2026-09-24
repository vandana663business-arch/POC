import { useNavigate } from "react-router-dom";
import { useTheme } from "../theme/ThemeContext";

function ShieldLogoIcon() {
  return (
    <svg width="26" height="30" viewBox="0 0 26 30" fill="none">
      <path
        d="M13 0 24 4.5v8.6c0 8-4.7 13.9-11 16.9C6.7 27 2 21.1 2 13.1V4.5L13 0Z"
        fill="#2f6bff"
      />
      <path
        d="M13 3.4 21.4 6.7v6.4c0 6.3-3.6 10.9-8.4 13.1-4.8-2.2-8.4-6.8-8.4-13.1V6.7L13 3.4Z"
        fill="#eaf1ff"
      />
      <path
        d="m8.6 14 3 3 5.8-6.2"
        stroke="#2f6bff"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  );
}

function BuildingIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <path
        d="M4 21V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v16M4 21h16M13 21v-5h5a1 1 0 0 1 1 1v4M8 8h1M8 12h1M8 16h1M11 8h1M11 12h1M11 16h1"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function SunIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="4.5" stroke="currentColor" strokeWidth="1.8" />
      <path
        d="M12 2v2.4M12 19.6V22M4.9 4.9l1.7 1.7M17.4 17.4l1.7 1.7M2 12h2.4M19.6 12H22M4.9 19.1l1.7-1.7M17.4 6.6l1.7-1.7"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
    </svg>
  );
}

function MoonIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <path
        d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinejoin="round"
        fill="currentColor"
        fillOpacity="0"
      />
    </svg>
  );
}

function HelpIcon() {
  return (
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="9.5" stroke="currentColor" strokeWidth="1.6" />
      <path
        d="M9.5 9.3a2.5 2.5 0 1 1 3.7 2.2c-.8.5-1.2 1-1.2 1.9"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
      />
      <circle cx="12" cy="16.8" r="1" fill="currentColor" />
    </svg>
  );
}

function UserIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="1.6" />
      <path d="M4.5 20a7.5 7.5 0 0 1 15 0" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

function ChevronDownIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
      <path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function InboxIcon() {
  return (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
      <path d="M8 26h9l3 5h8l3-5h9v13a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2V26Z" fill="#3f74ff" />
      <path d="M8 26 13 10a2 2 0 0 1 2-1.5h18a2 2 0 0 1 2 1.5l5 16" stroke="#3f74ff" strokeWidth="2" fill="none" strokeLinejoin="round" />
      <rect x="19" y="12" width="10" height="13" rx="1.5" fill="#dce7ff" />
      <path d="M21 16h6M21 19.5h6" stroke="#3f74ff" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M24 18.5v6.5m0 0-3-3m3 3 3-3" stroke="#3f74ff" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function ShieldHeartIcon() {
  return (
    <svg width="46" height="48" viewBox="0 0 46 48" fill="none">
      <path
        d="M23 2 41 8v13c0 12-7.6 20.6-18 24.5C12.6 41.6 5 33 5 21V8L23 2Z"
        stroke="currentColor"
        strokeWidth="2.2"
        fill="none"
      />
      <path
        d="M9 22h6l3-6 4 11 3-7h9"
        stroke="currentColor"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  );
}

function LockIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <rect x="4.5" y="10.5" width="15" height="10" rx="2" stroke="currentColor" strokeWidth="1.6" />
      <path d="M8 10.5V7.5a4 4 0 0 1 8 0v3" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
      <circle cx="12" cy="15.2" r="1.4" fill="currentColor" />
    </svg>
  );
}

function PeopleIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <circle cx="9" cy="8" r="3" stroke="currentColor" strokeWidth="1.6" />
      <path d="M3 20a6 6 0 0 1 12 0" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
      <path d="M16 8.5a2.7 2.7 0 1 1 0-5.4M18.5 20a5.2 5.2 0 0 0-3.8-6.3" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

function InfoIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" fill="currentColor" />
      <path d="M12 11v6" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
      <circle cx="12" cy="7.5" r="1.3" fill="#fff" />
    </svg>
  );
}

function ArrowRightIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function LandingBackground() {
  return (
    <svg className="landing-bg" viewBox="0 0 1672 941" preserveAspectRatio="none">
      <path
        d="M-100 700c250-140 430-140 620 0s430 140 620 0 430-140 620 0"
        stroke="var(--accent)"
        strokeWidth="2"
        fill="none"
        opacity="0.35"
      />
      <path
        d="M-100 780c250-140 430-140 620 0s430 140 620 0 430-140 620 0"
        stroke="var(--accent)"
        strokeWidth="2"
        fill="none"
        opacity="0.22"
      />
      <path
        d="M-100 150c250 140 430 140 620 0s430-140 620 0 430 140 620 0"
        stroke="var(--accent)"
        strokeWidth="2"
        fill="none"
        opacity="0.18"
      />
    </svg>
  );
}

export default function Landing() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();

  return (
    <div className="landing">
      <LandingBackground />

      <header className="landing-header">
        <div className="landing-brand">
          <ShieldLogoIcon />
          <div className="landing-brand-name">
            <b>BCBS</b>
            <span>MINNESOTA</span>
          </div>
          <div className="landing-brand-divider" />
          <div className="landing-brand-title">BCBS MN Process</div>
        </div>

        <div className="landing-header-right">
          <div className="landing-org">
            <BuildingIcon />
            <span>Philippines Operations</span>
            <span className="landing-org-divider" />
            <span className="landing-org-muted">PHT</span>
          </div>

          <div className="landing-toggle">
            <button
              type="button"
              className={theme === "light" ? "active" : ""}
              onClick={() => setTheme("light")}
              aria-label="Light mode"
            >
              <SunIcon />
            </button>
            <button
              type="button"
              className={theme === "dark" ? "active" : ""}
              onClick={() => setTheme("dark")}
              aria-label="Dark mode"
            >
              <MoonIcon />
            </button>
          </div>

          <button type="button" className="landing-icon-btn" aria-label="Help">
            <HelpIcon />
          </button>

          <div className="landing-avatar">
            <div className="landing-avatar-circle">
              <UserIcon />
            </div>
            <ChevronDownIcon />
          </div>
        </div>
      </header>

      <div className="landing-hero">
        <div className="landing-eyebrow">PROCESS WORKSPACE</div>
        <h1>Choose where you want to begin</h1>
        <p>Select a process to continue.</p>
      </div>

      <div className="landing-cards">
        <div className="process-card featured">
          <div className="process-icon">
            <InboxIcon />
          </div>
          <h3>Intake</h3>
          <p>Forecast case volumes and staffing needs.</p>
          <span className="process-status available">
            <span className="status-dot" />
            Available
          </span>
          <button type="button" className="process-action primary" onClick={() => navigate("/intake")}>
            Open Intake
            <ArrowRightIcon />
          </button>
          <div className="process-hint">Press Enter to open</div>
        </div>

        <div className="process-card disabled">
          <div className="process-tooltip-anchor">
            <div className="process-icon">
              <ShieldHeartIcon />
            </div>
            <div className="process-tooltip">
              <span className="process-tooltip-icon">
                <InfoIcon />
              </span>
              Clinical will be available soon
            </div>
          </div>
          <h3>Clinical</h3>
          <p>Clinical workforce planning and insights.</p>
          <span className="process-status soon">
            <span className="status-dot" />
            Coming soon
          </span>
          <button type="button" className="process-action disabled" disabled>
            Preview
          </button>
        </div>
      </div>

      <div className="landing-footer">
        <div className="landing-footer-item">
          <LockIcon />
          Secure workspace
        </div>
        <div className="landing-footer-divider" />
        <div className="landing-footer-item">
          <PeopleIcon />
          Role-based access
        </div>
        <div className="landing-footer-divider" />
        <div className="landing-footer-item">
          <BuildingIcon />
          Philippines Operations
        </div>
      </div>

      <div className="landing-caption">Internal planning tool</div>
    </div>
  );
}
