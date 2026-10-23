import React, { useState, useEffect } from "react";
import * as XLSX from "xlsx";

export default function DataManager({ title, fields }) {
  const storageKey = `mai_nexus_${title.toLowerCase().replace(/\s+/g, "_")}`;

  const [dataList, setDataList] = useState([]);
  const [formData, setFormData] = useState({});
  const [showForm, setShowForm] = useState(false);

  // Ambil Profil Sekolah dari LocalStorage untuk Kop Surat & Tanda Tangan
  const [schoolProfile, setSchoolProfile] = useState({
    namaSekolah: "SEKOLAH DEMO MAI NEXUS",
    npsn: "12345678",
    alamat: "Jl. Edukasi No. 1, Kota Bandung Barat",
    kepalaSekolah: "Drs. H. Nama Kepala Sekolah, M.Pd.",
  });

  useEffect(() => {
    const savedData = localStorage.getItem(storageKey);
    if (savedData) {
      try {
        setDataList(JSON.parse(savedData));
      } catch (e) {
        console.error(e);
      }
    }

    const savedProfile = localStorage.getItem("mai_nexus_settings_profile");
    if (savedProfile) {
      try {
        const parsed = JSON.parse(savedProfile);
        setSchoolProfile((prev) => ({
          ...prev,
          namaSekolah: parsed.namaSekolah || prev.namaSekolah,
          npsn: parsed.npsn || prev.npsn,
          alamat: parsed.alamat || prev.alamat,
          kepalaSekolah: parsed.kepalaSekolah || prev.kepalaSekolah,
        }));
      } catch (e) {
        console.error(e);
      }
    }
  }, [storageKey]);

  const saveData = (newList) => {
    setDataList(newList);
    localStorage.setItem(storageKey, JSON.stringify(newList));
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAddData = (e) => {
    e.preventDefault();
    const updated = [...dataList, formData];
    saveData(updated);
    setFormData({});
    setShowForm(false);
  };

  const handleDeleteData = (index) => {
    const updated = dataList.filter((_, i) => i !== index);
    saveData(updated);
  };

  // Upload Excel
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const bstr = evt.target.result;
        const wb = XLSX.read(bstr, { type: "binary" });
        const wsname = wb.SheetNames[0];
        const ws = wb.Sheets[wsname];
        const parsedData = XLSX.utils.sheet_to_json(ws);

        if (parsedData.length > 0) {
          const updated = [...dataList, ...parsedData];
          saveData(updated);
          alert(`Berhasil mengunggah ${parsedData.length} data baru!`);
        }
      } catch (err) {
        alert("Gagal membaca file. Pastikan format file .xlsx atau .csv sudah benar.");
      }
    };
    reader.readAsBinaryString(file);
    e.target.value = "";
  };

  // Export Excel
  const handleExportExcel = () => {
    if (dataList.length === 0) {
      alert("Tidak ada data untuk diekspor.");
      return;
    }
    const worksheet = XLSX.utils.json_to_sheet(dataList);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, title);
    XLSX.writeFile(workbook, `Laporan_${title}_MAI_Nexus.xlsx`);
  };

  // Print PDF / Browser Print
  const handlePrint = () => {
    window.print();
  };

  const currentDateStr = new Date().toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="data-manager-container" style={{ padding: "16px", fontFamily: "sans-serif" }}>
      {/* CSS KHUSUS PRINT CETAK LAPORAN */}
      <style>{`
        @media print {
          body * {
            visibility: hidden;
          }
          .printable-area, .printable-area * {
            visibility: visible;
          }
          .printable-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
          }
          .no-print {
            display: none !important;
          }
          .print-header {
            display: block !important;
            text-align: center;
            border-bottom: 3px double #000;
            padding-bottom: 12px;
            margin-bottom: 20px;
          }
          .print-footer {
            display: flex !important;
            justify-content: flex-end;
            margin-top: 40px;
            page-break-inside: avoid;
          }
          table {
            width: 100%;
            border-collapse: collapse;
          }
          th, td {
            border: 1px solid #000 !important;
            padding: 8px !important;
            font-size: 12px !important;
          }
          th.action-col, td.action-col {
            display: none !important;
          }
        }
        .print-header, .print-footer {
          display: none;
        }
      `}</style>

      {/* Header Aksi (Disembunyikan saat Print) */}
      <div className="no-print" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", flexWrap: "wrap", gap: "10px" }}>
        <h2 style={{ fontSize: "18px", fontWeight: "bold", margin: 0, color: "#1e293b" }}>
          Manajemen Data {title}
        </h2>
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
          <button
            onClick={() => setShowForm(!showForm)}
            style={{ backgroundColor: "#2563eb", color: "#fff", border: "none", padding: "8px 14px", borderRadius: "6px", fontWeight: "600", fontSize: "12px", cursor: "pointer" }}
          >
            {showForm ? "Tutup Form" : "+ Tambah Manual"}
          </button>

          <label style={{ backgroundColor: "#10b981", color: "#fff", padding: "8px 14px", borderRadius: "6px", fontWeight: "600", fontSize: "12px", cursor: "pointer", display: "inline-block" }}>
            📂 Upload Excel
            <input type="file" accept=".xlsx, .xls, .csv" onChange={handleFileUpload} style={{ display: "none" }} />
          </label>

          <button
            onClick={handleExportExcel}
            style={{ backgroundColor: "#0284c7", color: "#fff", border: "none", padding: "8px 14px", borderRadius: "6px", fontWeight: "600", fontSize: "12px", cursor: "pointer" }}
          >
            📥 Export Excel
          </button>

          <button
            onClick={handlePrint}
            style={{ backgroundColor: "#475569", color: "#fff", border: "none", padding: "8px 14px", borderRadius: "6px", fontWeight: "600", fontSize: "12px", cursor: "pointer" }}
          >
            🖨️ Cetak PDF
          </button>
        </div>
      </div>

      {/* Form Input Manual */}
      {showForm && (
        <form className="no-print" onSubmit={handleAddData} style={{ backgroundColor: "#f8fafc", padding: "16px", borderRadius: "10px", border: "1px solid #e2e8f0", marginBottom: "16px" }}>
          <h4 style={{ margin: "0 0 12px 0", fontSize: "14px", color: "#334155" }}>Input Data Baru ({title})</h4>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "10px", marginBottom: "12px" }}>
            {fields.map((f) => (
              <div key={f.key}>
                <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#64748b", marginBottom: "4px" }}>
                  {f.label.toUpperCase()}
                </label>
                <input
                  type="text"
                  name={f.key}
                  value={formData[f.key] || ""}
                  onChange={handleInputChange}
                  required
                  style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
                />
              </div>
            ))}
          </div>
          <button type="submit" style={{ backgroundColor: "#2563eb", color: "#fff", border: "none", padding: "8px 16px", borderRadius: "6px", fontWeight: "bold", fontSize: "12px", cursor: "pointer" }}>
            Simpan Data
          </button>
        </form>
      )}

      {/* AREA UTAMA YANG AKAN DICETAK PADA PDF / PRINT */}
      <div className="printable-area" style={{ backgroundColor: "#ffffff", padding: "16px", borderRadius: "10px", border: "1px solid #e2e8f0" }}>
        
        {/* KOP SURAT FORMAL SEKOLAH */}
        <div className="print-header">
          <h2 style={{ margin: "0", fontSize: "18px", textTransform: "uppercase", letterSpacing: "1px" }}>
            {schoolProfile.namaSekolah}
          </h2>
          <p style={{ margin: "2px 0", fontSize: "12px" }}>
            NPSN: {schoolProfile.npsn || "-"} | Alamat: {schoolProfile.alamat || "-"}
          </p>
          <hr style={{ border: "none", borderTop: "2px solid #000", marginTop: "10px" }} />
          <h3 style={{ margin: "10px 0 0 0", fontSize: "14px", textDecoration: "underline" }}>
            LAPORAN DATA {title.toUpperCase()}
          </h3>
        </div>

        {/* TABEL DATA */}
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "13px" }}>
            <thead>
              <tr style={{ backgroundColor: "#f1f5f9", borderBottom: "2px solid #cbd5e1" }}>
                <th style={{ padding: "10px", width: "40px", textCenter: "center" }}>No</th>
                {fields.map((f) => (
                  <th key={f.key} style={{ padding: "10px", color: "#334155" }}>
                    {f.label}
                  </th>
                ))}
                <th className="action-col" style={{ padding: "10px", width: "50px", textAlign: "center" }}>Aksi</th>
              </tr>
            </thead>
            <tbody>
              {dataList.length === 0 ? (
                <tr>
                  <td colSpan={fields.length + 2} style={{ padding: "20px", textAlign: "center", color: "#94a3b8" }}>
                    Belum ada data. Silakan tambah manual atau upload Excel.
                  </td>
                </tr>
              ) : (
                dataList.map((row, idx) => (
                  <tr key={idx} style={{ borderBottom: "1px solid #e2e8f0" }}>
                    <td style={{ padding: "10px", textAlign: "center" }}>{idx + 1}</td>
                    {fields.map((f) => (
                      <td key={f.key} style={{ padding: "10px", color: "#1e293b" }}>
                        {row[f.key] || row[f.label] || row[f.key.toLowerCase()] || "-"}
                      </td>
                    ))}
                    <td className="action-col" style={{ padding: "10px", textAlign: "center" }}>
                      <button
                        onClick={() => handleDeleteData(idx)}
                        style={{ color: "#ef4444", background: "none", border: "none", fontWeight: "bold", cursor: "pointer", fontSize: "14px" }}
                        title="Hapus Data"
                      >
                        ×
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* TANDA TANGAN KEPALA SEKOLAH (PADA HASIL PRINT) */}
        <div className="print-footer">
          <div style={{
          
