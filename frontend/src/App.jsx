
import React, { useState } from "react";
import "./styles/global.css";
import EducationData from "./pages/EducationData";

const menuItems = [
  { id: "dashboard", label: "Dashboard", icon: "⌂" },
  { id: "schools", label: "Data Sekolah", icon: "▤" },
  { id: "students", label: "Data Siswa", icon: "♙" },
  { id: "academic-years", label: "Tahun Ajaran", icon: "▦" },
  { id: "classes", label: "Manajemen Kelas", icon: "▧" },
  { id: "teachers", label: "Data Guru", icon: "♧" },
  { id: "attendance", label: "Kehadiran", icon: "✓" },
  { id: "settings", label: "Pengaturan", icon: "⚙" },
];

const stats = [
  { label: "Total Siswa", value: "—", note: "Data dari API", icon: "♙" },
  { label: "Total Guru", value: "—", note: "Data dari API", icon: "♧" },
  { label: "Total Kelas", value: "—", note: "Data dari API", icon: "▦" },
  { label: "Tahun Ajaran", value: "—", note: "Data dari API", icon: "▤" },
];

export default function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const activeLabel =
    menuItems.find((item) => item.id === activePage)?.label || "Dashboard";

  const showEducationData =
    activePage === "schools" || activePage === "students";

  return (
    <div className="app-shell">
      {sidebarOpen && (
        <button
          className="sidebar-backdrop"
          aria-label="Tutup menu"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-mark">M</div>
          <div>
            <strong>MAI NEXUS AI</strong>
            <span>EDUCATION</span>
          </div>
          <button
            className="close-sidebar"
            onClick={() => setSidebarOpen(false)}
            aria-label="Tutup navigasi"
          >
            ×
          </button>
        </div>

        <div className="workspace-label">WORKSPACE</div>
        <div className="workspace">
          <div className="workspace-avatar">S</div>
          <div className="workspace-info">
            <strong>Sekolah Anda</strong>
            <span>Education Workspace</span>
          </div>
          <span className="workspace-arrow">⌄</span>
        </div>

        <nav className="nav-menu" aria-label="Navigasi utama">
          <div className="nav-heading">MENU UTAMA</div>
          {menuItems.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${
                activePage === item.id ? "nav-active" : ""
              }`}
              onClick={() => {
                setActivePage(item.id);
                setSidebarOpen(false);
              }}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
              {activePage === item.id && <span className="active-dot" />}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="online-indicator" />
          <span>MAI Nexus AI Education</span>
          <span className="version">v0.1</span>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="topbar-left">
            <button
              className="menu-toggle"
              onClick={() => setSidebarOpen(true)}
              aria-label="Buka navigasi"
            >
              ☰
            </button>
            <div className="breadcrumb">
              <span>Education</span>
              <span className="breadcrumb-separator">/</span>
              <strong>{activeLabel}</strong>
            </div>
          </div>

          <div className="topbar-right">
            <div className="topbar-date">
              <span className="status-dot" />
              Sistem Pendidikan
            </div>
            <div className="profile-avatar">A</div>
          </div>
        </header>

        <div className="page-content">
          <section className="welcome-row">
            <div>
              <div className="eyebrow">MAI NEXUS AI EDUCATION</div>
              <h1>
                {activePage === "dashboard"
                  ? "Dashboard Sekolah"
                  : activeLabel}
              </h1>
              <p>
                Kelola administrasi dan aktivitas akademik sekolah dalam satu
                platform terintegrasi.
              </p>
            </div>
            <div className="welcome-badge">
              <span className="welcome-badge-icon">✦</span>
              <div>
                <strong>AI-Powered Education</strong>
                <span>Human-in-the-Loop</span>
              </div>
            </div>
          </section>

          {activePage === "dashboard" ? (
            <>
              <section className="stats-grid">
                {stats.map((stat, index) => (
                  <article className="stat-card" key={stat.label}>
                    <div className="stat-top">
                      <span className={`stat-icon stat-icon-${index}`}>
                        {stat.icon}
                      </span>
                      <span className="stat-menu">•••</span>
                    </div>
                    <div className="stat-label">{stat.label}</div>
                    <div className="stat-value">{stat.value}</div>
                    <div className="stat-note">{stat.note}</div>
                  </article>
                ))}
              </section>

              <section className="content-grid">
                <article className="panel overview-panel">
                  <div className="panel-heading">
                    <div>
                      <h2>Ringkasan Akademik</h2>
                      <p>Ikhtisar operasional sekolah</p>
                    </div>
                    <span className="panel-icon">▥</span>
                  </div>

                  <div className="empty-state">
                    <div className="empty-icon">▤</div>
                    <strong>Menyiapkan data akademik</strong>
                    <p>
                      Statistik akan ditampilkan setelah frontend terhubung
                      dengan API backend.
                    </p>
                  </div>
                </article>

                <article className="panel quick-panel">
                  <div className="panel-heading">
                    <div>
                      <h2>Akses Cepat</h2>
                      <p>Menu operasional sekolah</p>
                    </div>
                  </div>

                  <div className="quick-links">
                    {menuItems.slice(1, 5).map((item) => (
                      <button
                        className="quick-link"
                        key={item.id}
                        onClick={() => setActivePage(item.id)}
                      >
                        <span className="quick-link-icon">{item.icon}</span>
                        <span>{item.label}</span>
                        <span className="quick-arrow">→</span>
                      </button>
                    ))}
                  </div>
                </article>
              </section>

              <section className="panel activity-panel">
                <div className="panel-heading">
                  <div>
                    <h2>Aktivitas Sistem</h2>
                    <p>Status awal antarmuka</p>
                  </div>
                  <span className="status-pill">UI Preview</span>
                </div>
                <div className="activity-row">
                  <div className="activity-icon">✓</div>
                  <div className="activity-copy">
                    <strong>Antarmuka dashboard</strong>
                    <span>Komponen navigasi dan tata letak tersedia.</span>
                  </div>
                  <span className="activity-time">UI</span>
                </div>
                <div className="activity-row">
                  <div className="activity-icon">↔</div>
                  <div className="activity-copy">
                    <strong>Integrasi API</strong>
                    <span>
                      Status koneksi akan diketahui ketika halaman data dibuka.
                    </span>
                  </div>
                  <span className="activity-time">API</span>
                </div>
              </section>
            </>
          ) : showEducationData ? (
            <EducationData key={activePage} />
          ) : (
            <section className="panel module-placeholder">
              <div className="module-placeholder-icon">
                {menuItems.find((item) => item.id === activePage)?.icon}
              </div>
              <h2>{activeLabel}</h2>
              <p>
                Area modul {activeLabel.toLowerCase()} telah disiapkan pada
                navigasi. Halaman ini belum terhubung dengan data backend.
              </p>
              <button
                className="primary-button"
                onClick={() => setActivePage("dashboard")}
              >
                Kembali ke Dashboard
              </button>
            </section>
          )}

          <footer className="page-footer">
            <span>© MAI Solution Hub</span>
            <span>MAI Nexus AI Education</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
