import React, { useState, useEffect } from "react";
import * as XLSX from "xlsx";

export default function FinancialManager() {
  const storageKey = "mai_nexus_keuangan";

  const [transactions, setTransactions] = useState([]);
  const [formData, setFormData] = useState({
    tanggal: new Date().toISOString().split("T")[0],
    jenis: "Pemasukan",
    kategori: "SPP Siswa",
    keterangan: "",
    jumlah: "",
  });
  const [showForm, setShowForm] = useState(false);

  // Profile Sekolah untuk Kop Surat
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
        setTransactions(JSON.parse(savedData));
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
  }, []);

  const saveTransactions = (newList) => {
    setTransactions(newList);
    localStorage.setItem(storageKey, JSON.stringify(newList));
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAddTransaction = (e) => {
    e.preventDefault();
    if (!formData.jumlah || isNaN(formData.jumlah)) {
      alert("Masukkan nominal jumlah yang valid!");
      return;
    }

    const updated = [
      ...transactions,
      { ...formData, jumlah: parseFloat(formData.jumlah) },
    ];
    saveTransactions(updated);
    setFormData({
      tanggal: new Date().toISOString().split("T")[0],
      jenis: "Pemasukan",
      kategori: "SPP Siswa",
      keterangan: "",
      jumlah: "",
    });
    setShowForm(false);
  };

  const handleDelete = (index) => {
    const updated = transactions.filter((_, i) => i !== index);
    saveTransactions(updated);
  };

  // Perhitungan Cash Flow
  const totalPemasukan = transactions
    .filter((t) => t.jenis === "Pemasukan")
    .reduce((acc, t) => acc + Number(t.jumlah || 0), 0);

  const totalPengeluaran = transactions
    .filter((t) => t.jenis === "Pengeluaran")
    .reduce((acc, t) => acc + Number(t.jumlah || 0), 0);

  const saldoKas = totalPemasukan - totalPengeluaran;

  const handleExportExcel = () => {
    if (transactions.length === 0) {
      alert("Tidak ada data transaksi untuk diekspor.");
      return;
    }
    const worksheet = XLSX.utils.json_to_sheet(transactions);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Laporan Keuangan");
    XLSX.writeFile(workbook, "Laporan_Keuangan_Sekolah_MAI_Nexus.xlsx");
  };

  const handlePrint = () => {
    window.print();
  };

  const formatRupiah = (number) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      maximumFractionDigits: 0,
    }).format(number);
  };

  const currentDateStr = new Date().toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="financial-manager-container" style={{ padding: "16px", fontFamily: "sans-serif" }}>
      <style>{`
        @media print {
          body * { visibility: hidden; }
          .printable-area, .printable-area * { visibility: visible; }
          .printable-area { position: absolute; left: 0; top: 0; width: 100%; }
          .no-print { display: none !important; }
          .print-header { display: block !important; text-align: center; border-bottom: 3px double #000; padding-bottom: 12px; margin-bottom: 20px; }
          .print-footer { display: flex !important; justify-content: flex-end; margin-top: 40px; page-break-inside: avoid; }
          table { width: 100%; border-collapse: collapse; }
          th, td { border: 1px solid #000 !important; padding: 8px !important; font-size: 12px !important; }
          th.action-col, td.action-col { display: none !important; }
        }
        .print-header, .print-footer { display: none; }
      `}</style>

      {/* Header & Aksi */}
      <div className="no-print" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", flexWrap: "wrap", gap: "10px" }}>
        <h2 style={{ fontSize: "18px", fontWeight: "bold", margin: 0, color: "#1e293b" }}>
          Laporan Keuangan & Cash Flow Sekolah
        </h2>
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
          <button
            onClick={() => setShowForm(!showForm)}
            style={{ backgroundColor: "#2563eb", color: "#fff", border: "none", padding: "8px 14px", borderRadius: "6px", fontWeight: "600", fontSize: "12px", cursor: "pointer" }}
          >
            {showForm ? "Tutup Form" : "+ Catat Transaksi"}
          </button>
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

      {/* Ringkasan Ringkas Cash Flow */}
      <div className="no-print" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "12px", marginBottom: "20px" }}>
        <div style={{ backgroundColor: "#ecfdf5", padding: "16px", borderRadius: "10px", border: "1px solid #a7f3d0" }}>
          <span style={{ fontSize: "12px", color: "#047857", fontWeight: "600" }}>Total Pemasukan</span>
          <h3 style={{ margin: "4px 0 0 0", color: "#065f46", fontSize: "18px" }}>{formatRupiah(totalPemasukan)}</h3>
        </div>
        <div style={{ backgroundColor: "#fef2f2", padding: "16px", borderRadius: "10px", border: "1px solid #fecaca" }}>
          <span style={{ fontSize: "12px", color: "#b91c1c", fontWeight: "600" }}>Total Pengeluaran</span>
          <h3 style={{ margin: "4px 0 0 0", color: "#991b1b", fontSize: "18px" }}>{formatRupiah(totalPengeluaran)}</h3>
        </div>
        <div style={{ backgroundColor: "#eff6ff", padding: "16px", borderRadius: "10px", border: "1px solid #bfdbfe" }}>
          <span style={{ fontSize: "12px", color: "#1d4ed8", fontWeight: "600" }}>Saldo Kas Saat Ini</span>
          <h3 style={{ margin: "4px 0 0 0", color: "#1e40af", fontSize: "18px" }}>{formatRupiah(saldoKas)}</h3>
        </div>
      </div>

      {/* Form Input Transaksi */}
      {showForm && (
        <form className="no-print" onSubmit={handleAddTransaction} style={{ backgroundColor: "#f8fafc", padding: "16px", borderRadius: "10px", border: "1px solid #e2e8f0", marginBottom: "16px" }}>
          <h4 style={{ margin: "0 0 12px 0", fontSize: "14px", color: "#334155" }}>Catat Transaksi Keuangan Baru</h4>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "10px", marginBottom: "12px" }}>
            <div>
              <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#64748b", marginBottom: "4px" }}>TANGGAL</label>
              <input type="date" name="tanggal" value={formData.tanggal} onChange={handleInputChange} required style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #cbd5e1", boxSizing: "border-box" }} />
            </div>
            <div>
              <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#64748b", marginBottom: "4px" }}>JENIS TRANSAKSI</label>
              <select name="jenis" value={formData.jenis} onChange={handleInputChange} style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}>
                <option value="Pemasukan">Pemasukan (+)</option>
                <option value="Pengeluaran">Pengeluaran (-)</option>
              </select>
            </div>
            <div>
              <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#64748b", marginBottom: "4px" }}>KATEGORI</label>
              <input type="text" name="kategori" placeholder="misal: SPP, Dana BOS, Gaji" value={formData.kategori} onChange={handleInputChange} required style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #cbd5e1", boxSizing: "border-box" }} />
            </div>
            <div>
              <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#64748b", marginBottom: "4px" }}>NOMINAL (RP)</label>
              <input type="number" name="jumlah" placeholder="misal: 500000" value={formData.jumlah} onChange={handleInputChange} required style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #cbd5e1", boxSizing: "border-box" }} />
            </div>
          </div>
          <div style={{ marginBottom: "12px" }}>
            <label style={{ display: "block", fontSize: "11px", fontWeight: "bold", color: "#64748b", marginBottom: "4px" }}>KETERANGAN / URAIAN</label>
            <input type="text" name="keterangan" placeholder="Keterangan rincian transaksi..." value={formData.keterangan} onChange={handleInputChange} style={{ width: "100%", padding: "8px", borderRadius: "6px", border: "1px solid #cbd5e1", boxSizing: "border-box" }} />
          </div>
          <button type="submit" style={{ backgroundColor: "#2563eb", color: "#fff", border: "none", padding: "8px 16px", borderRadius: "6px", fontWeight: "bold", fontSize: "12px", cursor: "pointer" }}>Simpan Transaksi</button>
        </form>
      )}

      {/* Printable Area */}
      <div className="printable-area" style={{ backgroundColor: "#ffffff", padding: "16px", borderRadius: "10px", border: "1px solid #e2e8f0" }}>
        
        {/* Kop Surat */}
        <div className="print-header">
          <h2 style={{ margin: "0", fontSize: "18px", textTransform: "uppercase" }}>{schoolProfile.namaSekolah}</h2>
          <p style={{ margin: "2px 0", fontSize: "12px" }}>NPSN: {schoolProfile.npsn || "-"} | Alamat: {schoolProfile.alamat || "-"}</p>
          <hr style={{ border: "none", borderTop: "2px solid #000", marginTop: "10px" }} />
          <h3 style={{ margin: "10px 0 0 0", fontSize: "14px", textDecoration: "underline" }}>LAPORAN ARUS KAS (CASH FLOW) SEKOLAH</h3>
        </div>

        {/* Tabel Transaksi */}
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "13px" }}>
            <thead>
              <tr style={{ backgroundColor: "#f1f5f9", borderBottom: "2px solid #cbd5e1" }}>
                <th style={{ padding: "10px", width: "40px", textAlign: "center" }}>No</th>
                <th style={{ padding: "10px" }}>Tanggal</th>
                <th style={{ padding: "10px" }}>Jenis</th>
                <th style={{ padding: "10px" }}>Kategori</th>
                <th style={{ padding: "10px" }}>Keterangan</th>
                <th style={{ padding: "10px", textAlign: "right" }}>Jumlah (Rp)</th>
                <th className="action-col" style={{ padding: "10px", width: "50px", textAlign: "center" }}>Aksi</th>
              </tr>
            </thead>
            <tbody>
              {transactions.length === 0 ? (
                <tr>
                  <td colSpan="7" style={{ padding: "20px", textAlign: "center", color: "#94a3b8" }}>Belum ada data transaksi keuangan.</td>
                </tr>
              ) : (
                transactions.map((item, idx) => (
                  <tr key={idx} style={{ borderBottom: "1px solid #e2e8f0" }}>
                    <td style={{ padding: "10px", textAlign: "center" }}>{idx + 1}</td>
                    <td style={{ padding: "10px" }}>{item.tanggal}</td>
                    <td style={{ padding: "10px", fontWeight: "bold", color: item.jenis === "Pemasukan" ? "#059669" : "#dc2626" }}>{item.jenis}</td>
                    <td style={{ padding: "10px" }}>{item.kategori}</td>
                    <td style={{ padding: "10px" }}>{item.keterangan || "-"}</td>
                    <td style={{ padding: "10px", textAlign: "right", fontWeight: "600" }}>{formatRupiah(item.jumlah)}</td>
                    <td className="action-col" style={{ padding: "10px", textAlign: "center" }}>
                      <button onClick={() => handleDelete(idx)} style={{ color: "#ef4444", background: "none", border: "none", fontWeight: "bold", cursor: "pointer" }}>×</button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Tanda Tangan Print */}
        <div className="print-footer">
          <div style={{ textAlign: "center", width: "220px", fontSize: "12px" }}>
            <p style={{ margin: "0 0 60px 0" }}>Bandung Barat, {currentDateStr}<br />Kepala Sekolah,</p>
            <p style={{ margin: 0, fontWeight: "bold", textDecoration: "underline" }}>{schoolProfile.kepalaSekolah}</p>
            <p style={{ margin: 0 }}>NIP. ....................................</p>
          </div>
        </div>

      </div>
    </div>
  );
}
