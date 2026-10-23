import React, { useState, useEffect } from "react";

export default function SettingsPage() {
  const [schoolProfile, setSchoolProfile] = useState(() => {
    const saved = localStorage.getItem("mai_nexus_settings_profile");
    return saved
      ? JSON.parse(saved)
      : {
          namaSekolah: "Sekolah Anda",
          npsn: "",
          alamat: "",
          kepalaSekolah: "",
          aiApiKey: "",
          enableAiCopilot: true,
        };
  });

  const [savedStatus, setSavedStatus] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSchoolProfile((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSave = (e) => {
    e.preventDefault();
    localStorage.setItem(
      "mai_nexus_settings_profile",
      JSON.stringify(schoolProfile)
    );
    setSavedStatus(true);
    setTimeout(() => setSavedStatus(false), 3000);
  };

  const handleResetData = () => {
    if (
      window.confirm(
        "Apakah Anda yakin ingin menghapus SELURUH data lokal (Siswa, Guru, Kelas, dll)? Tindakan ini tidak dapat dibatalkan."
      )
    ) {
      Object.keys(localStorage).forEach((key) => {
        if (key.startsWith("mai_nexus_")) {
          localStorage.removeItem(key);
        }
      });
      alert("Seluruh data lokal berhasil dibersihkan!");
      window.location.reload();
    }
  };

  return (
    <div style={{ padding: "16px", fontFamily: "sans-serif", maxWidth: "800px" }}>
      <h2 style={{ fontSize: "18px", fontWeight: "bold", marginBottom: "16px", color: "#1e293b" }}>
        Pengaturan Sistem & Profil Sekolah
      </h2>

      {savedStatus && (
        <div style={{ padding: "12px", backgroundColor: "#d1fae5", color: "#065f46", borderRadius: "8px", marginBottom: "16px", fontSize: "14px" }}>
          ✓ Pengaturan berhasil disimpan!
        </div>
      )}

      <form onSubmit={handleSave}>
        {/* Profil Sekolah */}
        <div style={{ backgroundColor: "#ffffff", padding: "16px", borderRadius: "12px", border: "1px solid #e2e8f0", marginBottom: "20px" }}>
          <h3 style={{ fontSize: "15px", fontWeight: "bold", marginTop: 0, marginBottom: "12px", color: "#334155" }}>
            🏫 Profil Sekolah
          </h3>

          <div style={{ marginBottom: "12px" }}>
            <label style={{ display: "block", fontSize: "12px", fontWeight: "600", color: "#64748b", marginBottom: "4px" }}>
              NAMA SEKOLAH
            </label>
            <input
              type="text"
              name="namaSekolah"
              value={schoolProfile.namaSekolah}
              onChange={handleChange}
              style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
              required
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label style={{ display: "block", fontSize: "12px", fontWeight: "600", color: "#64748b", marginBottom: "4px" }}>
              NPSN
            </label>
            <input
              type="text"
              name="npsn"
              placeholder="Masukkan NPSN"
              value={schoolProfile.npsn}
              onChange={handleChange}
              style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label style={{ display: "block", fontSize: "12px", fontWeight: "600", color: "#64748b", marginBottom: "4px" }}>
              NAMA KEPALA SEKOLAH
            </label>
            <input
              type="text"
              name="kepalaSekolah"
              placeholder="Nama Kepala Sekolah beserta Gelar"
              value={schoolProfile.kepalaSekolah}
              onChange={handleChange}
              style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
            />
          </div>

          <div>
            <label style={{ display: "block", fontSize: "12px", fontWeight: "600", color: "#64748b", marginBottom: "4px" }}>
              ALAMAT LENGKAP
            </label>
            <textarea
              name="alamat"
              rows="2"
              placeholder="Alamat sekolah..."
              value={schoolProfile.alamat}
              onChange={handleChange}
              style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box", fontFamily: "sans-serif" }}
            />
          </div>
        </div>

        {/* Pengaturan AI Module */}
        <div style={{ backgroundColor: "#ffffff", padding: "16px", borderRadius: "12px", border: "1px solid #e2e8f0", marginBottom: "20px" }}>
          <h3 style={{ fontSize: "15px", fontWeight: "bold", marginTop: 0, marginBottom: "12px", color: "#334155" }}>
            🤖 Modul AI Copilot
          </h3>

          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
            <input
              type="checkbox"
              id="enableAiCopilot"
              name="enableAiCopilot"
              checked={schoolProfile.enableAiCopilot}
              onChange={handleChange}
              style={{ width: "18px", height: "18px" }}
            />
            <label htmlFor="enableAiCopilot" style={{ fontSize: "14px", fontWeight: "600", color: "#334155" }}>
              Aktifkan Asisten AI Teacher Copilot
            </label>
          </div>

          <div>
            <label style={{ display: "block", fontSize: "12px", fontWeight: "600", color: "#64748b", marginBottom: "4px" }}>
              API KEY (OPSIONAL / CUSTOM LLM)
            </label>
            <input
              type="password"
              name="aiApiKey"
              placeholder="Masukkan Gemini / OpenAI API Key"
              value={schoolProfile.aiApiKey}
              onChange={handleChange}
              style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
            />
          </div>
        </div>

        <button
          type="submit"
          style={{
            width: "100%",
            backgroundColor: "#2563eb",
            color: "#ffffff",
            padding: "12px",
            borderRadius: "8px",
            border: "none",
            fontWeight: "bold",
            fontSize: "14px",
            cursor: "pointer",
            marginBottom: "20px",
          }}
        >
          Simpan Pengaturan
        </button>
      </form>

      {/* Manajemen & Kebersihan Data */}
      <div style={{ backgroundColor: "#fef2f2", padding: "16px", borderRadius: "12px", border: "1px solid #fecaca" }}>
        <h3 style={{ fontSize: "15px", fontWeight: "bold", marginTop: 0, marginBottom: "6px", color: "#991b1b" }}>
          ⚠️ Zone Pembersihan Data
        </h3>
        <p style={{ fontSize: "12px", color: "#7f1d1d", marginTop: 0, marginBottom: "12px" }}>
          Tindakan ini akan menghapus semua simpanan data lokal (Siswa, Guru, Kelas, dll) di browser HP ini.
        </p>
        <button
          type="button"
          onClick={handleResetData}
          style={{
            backgroundColor: "#dc2626",
            color: "#ffffff",
            padding: "10px 16px",
            borderRadius: "8px",
            border: "none",
            fontWeight: "600",
            fontSize: "12px",
            cursor: "pointer",
          }}
        >
          Reset Seluruh Data Lokal
        </button>
      </div>
    </div>
  );
}
