import React, { useState, useEffect } from "react";

export default function StudentProgress() {
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Template Evaluasi AI
  const aiAnalysesList = [
    {
      akademik: "Memiliki pemahaman konsep logika yang sangat kuat dan konsisten dalam tugas harian.",
      perilaku: "Sangat disiplin, aktif memimpin diskusi kelompok, dan santun kepada guru.",
      catatanAI: "Siswa menunjukkan potensi kepemimpinan dan analitis yang menonjol. Disarankan untuk dilibatkan dalam kompetisi Sains/Matematika atau program pengayaan HOTS.",
    },
    {
      akademik: "Capaian nilai stabil di atas rata-rata kelas, namun perlu sedikit dorongan pada pemahaman soal cerita.",
      perilaku: "Kreatif, kooperatif dalam tim, dan selalu menyelesaikan tugas tepat waktu.",
      catatanAI: "Siswa merespons pembelajaran visual dengan sangat baik. Direkomendasikan media pembelajaran berbasis proyek (PBL) untuk mempertahankan minat belajarnya.",
    },
    {
      akademik: "Menunjukkan peningkatan signifikan pada pemahaman literasi dan bahasa.",
      perilaku: "Sopan, tekun, dan memiliki rasa empati yang tinggi terhadap sesama teman kelas.",
      catatanAI: "Perkembangan emosional dan akademiknya sangat seimbang. Disarankan orang tua memberikan apresiasi atas konsistensi usahanya di rumah.",
    },
  ];

  const [evalNotes, setEvalNotes] = useState(aiAnalysesList[0]);

  // Nilai Dummy
  const [grades, setGrades] = useState([
    { mapel: "Matematika", nilai: 88, predikat: "A" },
    { mapel: "Bahasa Indonesia", nilai: 90, predikat: "A" },
    { mapel: "IPA", nilai: 85, predikat: "B+" },
    { mapel: "Bahasa Inggris", nilai: 82, predikat: "B+" },
  ]);

  // Profil Sekolah dari LocalStorage
  const [schoolProfile, setSchoolProfile] = useState({
    namaSekolah: "SEKOLAH DEMO MAI NEXUS",
    npsn: "12345678",
    alamat: "Jl. Edukasi No. 1, Kota Bandung Barat",
    kepalaSekolah: "Drs. H. Nama Kepala Sekolah, M.Pd.",
  });

  useEffect(() => {
    const savedSiswa = localStorage.getItem("mai_nexus_siswa");
    if (savedSiswa) {
      try {
        const parsed = JSON.parse(savedSiswa);
        setStudents(parsed);
        if (parsed.length > 0) {
          setSelectedStudent(parsed[0]);
        }
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

  // Fungsi Simulasi Generate AI
  const handleGenerateAI = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      const randomIndex = Math.floor(Math.random() * aiAnalysesList.length);
      setEvalNotes(aiAnalysesList[randomIndex]);
      setIsAnalyzing(false);
    }, 1200);
  };

  const handlePrint = () => {
    window.print();
  };

  const currentDateStr = new Date().toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="student-progress-container" style={{ padding: "16px", fontFamily: "sans-serif" }}>
      <style>{`
        @media print {
          body * { visibility: hidden; }
          .printable-area, .printable-area * { visibility: visible; }
          .printable-area { position: absolute; left: 0; top: 0; width: 100%; }
          .no-print { display: none !important; }
          .print-header { display: block !important; text-align: center; border-bottom: 3px double #000; padding-bottom: 12px; margin-bottom: 20px; }
          .print-footer { display: flex !important; justify-content: space-between; margin-top: 50px; page-break-inside: avoid; }
          table { width: 100%; border-collapse: collapse; }
          th, td { border: 1px solid #000 !important; padding: 8px !important; font-size: 12px !important; }
        }
        .print-header, .print-footer { display: none; }
      `}</style>

      {/* Header & Aksi */}
      <div className="no-print" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", flexWrap: "wrap", gap: "10px" }}>
        <div>
          <h2 style={{ fontSize: "18px", fontWeight: "bold", margin: 0, color: "#1e293b" }}>
            Laporan Progres & Perkembangan Siswa
          </h2>
          <p style={{ fontSize: "12px", color: "#64748b", margin: 0 }}>
            Laporan evaluasi akademik dan karakter untuk disampaikan kepada Orang Tua / Wali.
          </p>
        </div>

        <div style={{ display: "flex", gap: "8px", alignItems: "center", flexWrap: "wrap" }}>
          {students.length > 0 && (
            <select
              onChange={(e) => {
                setSelectedStudent(students[e.target.value]);
                handleGenerateAI();
              }}
              style={{ padding: "8px", borderRadius: "6px", border: "1px solid #cbd5e1", fontSize: "12px" }}
            >
              {students.map((s, idx) => (
                <option key={idx} value={idx}>
                  {s.nama || s.nama_lengkap || "Siswa"} ({s.kelas || "Kelas"})
                </option>
              ))}
            </select>
          )}

          <button
            onClick={handleGenerateAI}
            disabled={isAnalyzing}
            style={{ backgroundColor: "#2563eb", color: "#fff", border: "none", padding: "8px 14px", borderRadius: "6px", fontWeight: "600", fontSize: "12px", cursor: "pointer" }}
          >
            {isAnalyzing ? "⚡ Menganalisis..." : "✨ Generate Analisis AI"}
          </button>

          <button
            onClick={handlePrint}
            style={{ backgroundColor: "#475569", color: "#fff", border: "none", padding: "8px 14px", borderRadius: "6px", fontWeight: "600", fontSize: "12px", cursor: "pointer" }}
          >
            🖨️ Cetak Rapor / PDF
          </button>
        </div>
      </div>

      {/* Printable Area */}
      <div className="printable-area" style={{ backgroundColor: "#ffffff", padding: "20px", borderRadius: "10px", border: "1px solid #e2e8f0" }}>
        
        {/* Kop Surat Sekolah */}
        <div className="print-header">
          <h2 style={{ margin: "0", fontSize: "18px", textTransform: "uppercase" }}>{schoolProfile.namaSekolah}</h2>
          <p style={{ margin: "2px 0", fontSize: "12px" }}>NPSN: {schoolProfile.npsn || "-"} | Alamat: {schoolProfile.alamat || "-"}</p>
          <hr style={{ border: "none", borderTop: "2px solid #000", marginTop: "10px" }} />
          <h3 style={{ margin: "10px 0 0 0", fontSize: "14px", textDecoration: "underline" }}>LAPORAN PERKEMBANGAN SISWA (RAPOR RINGKAS)</h3>
        </div>

        {/* Identitas Siswa */}
        <div style={{ backgroundColor: "#f8fafc", padding: "12px 16px", borderRadius: "8px", marginBottom: "16px", border: "1px solid #e2e8f0" }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", fontSize: "13px" }}>
            <div><strong>Nama Siswa:</strong> {selectedStudent ? (selectedStudent.nama || selectedStudent.nama_lengkap || "Budi Santoso") : "Budi Santoso"}</div>
            <div><strong>NISN:</strong> {selectedStudent ? (selectedStudent.nisn || "1001") : "1001"}</div>
            <div><strong>Kelas:</strong> {selectedStudent ? (selectedStudent.kelas || "7A") : "7A"}</div>
            <div><strong>Tahun Ajaran:</strong> 2025/2026 Ganjil</div>
          </div>
        </div>

        {/* Tabel Nilai Akademik */}
        <h4 style={{ margin: "16px 0 8px 0", fontSize: "14px", color: "#1e293b" }}>1. Ringkasan Capaian Akademik</h4>
        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "13px", marginBottom: "16px" }}>
          <thead>
            <tr style={{ backgroundColor: "#f1f5f9", borderBottom: "2px solid #cbd5e1" }}>
              <th style={{ padding: "8px", width: "40px", textAlign: "center" }}>No</th>
              <th style={{ padding: "8px" }}>Mata Pelajaran</th>
              <th style={{ padding: "8px", textAlign: "center", width: "100px" }}>Nilai Akhir</th>
              <th style={{ padding: "8px", textAlign: "center", width: "80px" }}>Predikat</th>
            </tr>
          </thead>
          <tbody>
            {grades.map((g, idx) => (
              <tr key={idx} style={{ borderBottom: "1px solid #e2e8f0" }}>
                <td style={{ padding: "8px", textAlign: "center" }}>{idx + 1}</td>
                <td style={{ padding: "8px" }}>{g.mapel}</td>
                <td style={{ padding: "8px", textAlign: "center", fontWeight: "bold" }}>{g.nilai}</td>
                <td style={{ padding: "8px", textAlign: "center" }}>{g.predikat}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Kehadiran Siswa */}
        <h4 style={{ margin: "16px 0 8px 0", fontSize: "14px", color: "#1e293b" }}>2. Rekapitulasi Kehadiran</h4>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "10px", textAlign: "center", marginBottom: "16px" }}>
          <div style={{ border: "1px solid #cbd5e1", padding: "8px", borderRadius: "6px" }}>
            <span style={{ fontSize: "11px", color: "#64748b", display: "block" }}>Hadir</span>
            <strong style={{ fontSize: "14px", color: "#16a34a" }}>95%</strong>
          </div>
          <div style={{ border: "1px solid #cbd5e1", padding: "8px", borderRadius: "6px" }}>
            <span style={{ fontSize: "11px", color: "#64748b", display: "block" }}>Sakit</span>
            <strong style={{ fontSize: "14px", color: "#0284c7" }}>2 Hari</strong>
          </div>
          <div style={{ border: "1px solid #cbd5e1", padding: "8px", borderRadius: "6px" }}>
            <span style={{ fontSize: "11px", color: "#64748b", display: "block" }}>Izin</span>
            <strong style={{ fontSize: "14px", color: "#d97706" }}>1 Hari</strong>
          </div>
          <div style={{ border: "1px solid #cbd5e1", padding: "8px", borderRadius: "6px" }}>
            <span style={{ fontSize: "11px", color: "#64748b", display: "block" }}>Alpa</span>
            <strong style={{ fontSize: "14px", color: "#dc2626" }}>0 Hari</strong>
          </div>
        </div>

        {/* Catatan Evaluasi & Rekomendasi AI */}
        <h4 style={{ margin: "16px 0 8px 0", fontSize: "14px", color: "#1e293b" }}>3. Catatan Perkembangan & Analisis AI</h4>
        <div style={{ border: "1px solid #cbd5e1", borderRadius: "8px", padding: "12px", fontSize: "12px", lineHeight: "1.6", backgroundColor: isAnalyzing ? "#f1f5f9" : "#fff" }}>
          {isAnalyzing ? (
            <p style={{ margin: 0, fontStyle: "italic", color: "#2563eb" }}>
              ⚡ AI sedang menganalisis rekap nilai dan kehadiran siswa...
            </p>
          ) : (
            <>
              <p style={{ margin: "0 0 8px 0" }}>
                <strong>• Catatan Akademik & Sikap:</strong> {evalNotes.akademik} {evalNotes.perilaku}
              </p>
              <p style={{ margin: 0, color: "#1d4ed8", fontStyle: "italic" }}>
                <strong>🤖 Rekomendasi MAI Nexus AI:</strong> {evalNotes.catatanAI}
              </p>
            </>
          )}
        </div>

        {/* Tanda Tangan */}
        <div className="print-footer">
          <div style={{ textAlign: "center", width: "200px", fontSize: "12px" }}>
            <p style={{ margin: "0 0 60px 0" }}>Mengetahui,<br />Orang Tua / Wali Siswa</p>
            <p style={{ margin: 0, fontWeight: "bold" }}>( .................................... )</p>
          </div>

          <div style={{ textAlign: "center", width: "200px", fontSize: "12px" }}>
            <p style={{ margin: "0 0 60px 0" }}>Bandung Barat, {currentDateStr}<br />Wali Kelas,</p>
            <p style={{ margin: 0, fontWeight: "bold", textDecoration: "underline" }}>{schoolProfile.kepalaSekolah}</p>
            <p style={{ margin: 0 }}>NIP. ....................................</p>
          </div>
        </div>

      </div>
    </div>
  );
      }
          
