import React, { useState, useEffect } from "react";
import "./styles/global.css";
import DataManager from "./components/DataManager";
import SettingsPage from "./components/SettingsPage";
import AiCopilot from "./components/AiCopilot";

const menuItems = [
  { id: "dashboard", label: "Dashboard", icon: "⌂" },
  { id: "ai-copilot", label: "AI Copilot", icon: "🤖" }, // <-- Ditambahkan di sini
  { id: "schools", label: "Data Sekolah", icon: "▤" },
  { id: "students", label: "Data Siswa", icon: "♙" },
  { id: "academic-years", label: "Tahun Ajaran", icon: "▦" },
  { id: "classes", label: "Manajemen Kelas", icon: "▧" },
  { id: "teachers", label: "Data Guru", icon: "♧" },
  { id: "attendance", label: "Kehadiran", icon: "✓" },
  { id: "settings", label: "Pengaturan", icon: "⚙" },
];

const moduleConfigs = {
  schools: {
    title: "Sekolah",
    fields: [
      { key: "npsn", label: "NPSN" },
      { key: "nama_sekolah", label: "Nama Sekolah" },
      { key: "alamat", label: "Alamat" },
    ],
  },
  students: {
    title: "Siswa",
    fields: [
      { key: "nisn", label: "NISN" },
      { key: "nama", label: "Nama Lengkap" },
      { key: "kelas", label: "Kelas" },
    ],
  },
  "academic-years": {
    title: "Tahun Ajaran",
    fields: [
      { key: "kode", label: "Kode" },
      { key: "tahun", label: "Tahun Ajaran" },
      { key: "status", label: "Status" },
    ],
  },
  classes: {
    title: "Kelas",
    fields: [
      { key: "kode_kelas", label: "Kode Kelas" },
      { key: "nama_kelas", label: "Nama Kelas" },
      { key: "wali_kelas", label: "Wali Kelas" },
    ],
  },
  teachers: {
    title: "Guru",
    fields: [
      { key: "nip", label: "NIP/NIK" },
      { key: "nama", label: "Nama Guru" },
      { key: "mapel", label: "Mata Pelajaran" },
    ],
  },
  attendance: {
    title: "Kehadiran",
    fields: [
      { key: "tanggal", label: "Tanggal" },
      { key: "nama_siswa", label: "Nama Siswa" },
      { key: "status", label: "Status (Hadir/Izin/Sakit)" },
    ],
  },
};

export default function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // State untuk menghitung jumlah data secara dinamis dari localStorage
  const [counts, setCounts] = useState({
    students: 0,
    teachers: 0,
    classes: 0,
    academicYears: 0,
  });

  useEffect(() => {
    try {
      const getLen = (key) => {
        const d = localStorage.getItem(`mai_nexus_${key}`);
        return d ? JSON.parse(d).length : 0;
      };

      setCounts({
        students: getLen("siswa"),
        teachers: getLen("guru"),
        classes: getLen("kelas"),
        academicYears: getLen("tahun_ajaran"),
      });
    } catch (e) {
      console.error(e);
    }
  }, [activePage]);

  const stats = [
    { label: "Total Siswa", value: counts.students, note: "Data Lokal Aktif", icon: "♙" },
    { label: "Total Guru", value: counts.teachers, note: "Data Lokal Aktif", icon: "♧" },
    { label: "Total Kelas", value: counts.classes, note: "Data Lokal Aktif", icon: "▦" },
    { label: "Tahun Ajaran", value: counts.academicYears, note: "Data Lokal Aktif", icon: "▤" },
  ];

  const activeLabel =
    menuItems.find((item) => item.id === activePage)?.label || "Dashboard";

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
          </section>

          {activePage === "dashboard" ? (
            // ... (bagian kode untuk Tampilan Dashboard) ...
          ) : activePage === "ai-copilot" ? (
            <AiCopilot />
          ) : activePage === "settings" ? (
            <SettingsPage />
          ) : moduleConfigs[activePage] ? (
            <DataManager
              key={activePage}
              title={moduleConfigs[activePage].title}
              fields={moduleConfigs[activePage].fields}
            />
          ) : (
            // ... (bagian untuk placeholder modul lain) ...
          )}

          <footer className="page-footer">
            <span>© MAI Solution Hub</span>
            <span>MAI Nexus AI Education</span>
          </footer>
        </div>


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
                    <strong>Sistem Aktif & Siap Digunakan</strong>
                    <p>
                      Data administrasi yang Anda input atau unggah dari Excel akan otomatis direkap di sistem lokal.
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
            </>
          ) : activePage === "settings" ? (
            <SettingsPage />
          ) : moduleConfigs[activePage] ? (
            <DataManager
              key={activePage}
              title={moduleConfigs[activePage].title}
              fields={moduleConfigs[activePage].fields}
            />
          ) : (
            <section className="panel module-placeholder">
              <h2>{activeLabel}</h2>
              <p>Modul {activeLabel} sedang disiapkan.</p>
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
