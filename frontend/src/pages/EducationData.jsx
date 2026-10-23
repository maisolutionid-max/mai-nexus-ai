
import React, { useCallback, useEffect, useState } from "react";
import api from "../services/api";
import React from 'react';
import DataManager from '../components/DataManager';

// Konfigurasi kolom untuk halaman Data Sekolah atau Edukasi umum
const schoolFields = [
  { key: 'npsn', label: 'NPSN' },
  { key: 'nama_sekolah', label: 'Nama Sekolah' },
  { key: 'alamat', label: 'Alamat' }
];

export default function EducationData() {
  return (
    <DataManager 
      title="Sekolah" 
      fields={schoolFields} 
    />
  );
}

const initialSchool = {
  name: "",
  npsn: "",
  school_level: "SMA",
  school_type: "general",
  address: "",
  is_active: true,
};

const initialStudent = {
  student_number: "",
  full_name: "",
  school_id: "",
  is_active: true,
};

const headers = [
  "student_number",
  "full_name",
  "school_id",
  "is_active",
];

const styles = {
  page: { display: "grid", gap: 20, color: "#172033" },
  panel: {
    padding: 20,
    background: "#fff",
    border: "1px solid #e1e6ef",
    borderRadius: 14,
    minWidth: 0,
  },
  tabs: { display: "flex", flexWrap: "wrap", gap: 8 },
  button: {
    padding: "11px 15px",
    border: "1px solid #14213d",
    borderRadius: 8,
    background: "#14213d",
    color: "#fff",
    cursor: "pointer",
    fontWeight: 600,
  },
  secondary: {
    padding: "10px 14px",
    border: "1px solid #ccd4e1",
    borderRadius: 8,
    background: "#fff",
    color: "#172033",
    cursor: "pointer",
  },
  field: { display: "grid", gap: 7, minWidth: 0 },
  input: {
    width: "100%",
    minWidth: 0,
    boxSizing: "border-box",
    padding: 11,
    border: "1px solid #ccd4e1",
    borderRadius: 8,
    background: "#fff",
    color: "#172033",
    font: "inherit",
  },
  form: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: 16,
  },
  tableWrap: { width: "100%", overflowX: "auto" },
  table: { width: "100%", minWidth: 480, borderCollapse: "collapse" },
  cell: {
    padding: 10,
    borderBottom: "1px solid #edf0f5",
    textAlign: "left",
    fontSize: 14,
  },
};

function Field({ label, children }) {
  return (
    <label style={styles.field}>
      <span style={{ fontSize: 14, fontWeight: 600 }}>{label}</span>
      {children}
    </label>
  );
}

function getErrorMessage(error) {
  const detail = error?.response?.data?.detail;

  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || "Data tidak valid").join("; ");
  }
  if (typeof detail === "string") return detail;
  if (detail && typeof detail === "object") {
    return detail.message || JSON.stringify(detail);
  }
  if (!error?.response) {
    return "Backend tidak dapat dihubungi. Periksa URL API dan koneksi.";
  }
  if (error.response.status === 401) return "Silakan login kembali.";
  if (error.response.status === 403) return "Akun tidak memiliki izin.";
  return `Permintaan gagal (${error.response.status}).`;
}

function asList(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.items)) return data.items;
  if (Array.isArray(data?.data)) return data.data;
  return [];
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function downloadCsvTemplate() {
  const rows = [
    headers,
    ["S-0001", "Nama Contoh", "1", "TRUE"],
  ];
  const csv = rows
    .map((row) =>
      row.map((value) => `"${String(value).replace(/"/g, '""')}"`).join(",")
    )
    .join("\r\n");

  downloadBlob(
    new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" }),
    "template_data_siswa.csv"
  );
}

function Table({ columns, rows, emptyMessage }) {
  return (
    <div style={styles.tableWrap}>
      <table style={styles.table}>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.label} style={styles.cell}>
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td colSpan={columns.length} style={styles.cell}>
                {emptyMessage}
              </td>
            </tr>
          ) : (
            rows.map((row, index) => (
              <tr key={row.id ?? `${row.row ?? "item"}-${index}`}>
                {columns.map((column) => (
                  <td key={column.label} style={styles.cell}>
                    {column.render
                      ? column.render(row)
                      : row[column.key] ?? "—"}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default function EducationData() {
  const [tab, setTab] = useState("schools");
  const [schools, setSchools] = useState([]);
  const [students, setStudents] = useState([]);
  const [schoolForm, setSchoolForm] = useState(initialSchool);
  const [studentForm, setStudentForm] = useState(initialStudent);
  const [file, setFile] = useState(null);
  const [importResult, setImportResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const loadData = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [schoolRes, studentRes] = await Promise.all([
        api.get("/education/schools"),
        api.get("/education/students"),
      ]);
      setSchools(asList(schoolRes.data));
      setStudents(asList(studentRes.data));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  function updateSchool(key, value) {
    setSchoolForm((old) => ({ ...old, [key]: value }));
  }

  function updateStudent(key, value) {
    setStudentForm((old) => ({ ...old, [key]: value }));
  }

  async function createSchool(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setNotice("");

    try {
      await api.post("/education/schools", {
        name: schoolForm.name.trim(),
        npsn: schoolForm.npsn.trim() || null,
        school_level: schoolForm.school_level,
        school_type: schoolForm.school_type,
        address: schoolForm.address.trim() || null,
        is_active: schoolForm.is_active,
      });
      setSchoolForm({ ...initialSchool });
      setNotice("Data sekolah berhasil disimpan.");
      await loadData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  }

  async function createStudent(event) {
    event.preventDefault();
    setError("");
    setNotice("");

    const payload = {
      student_number: studentForm.student_number.trim(),
      full_name: studentForm.full_name.trim(),
      school_id: Number(studentForm.school_id),
      is_active: studentForm.is_active,
    };

    if (
      !payload.student_number ||
      !payload.full_name ||
      !Number.isInteger(payload.school_id) ||
      payload.school_id <= 0
    ) {
      setError("Nomor siswa, nama, dan sekolah wajib diisi.");
      return;
    }

    setSaving(true);
    try {
      await api.post("/education/students", payload);
      setStudentForm({ ...initialStudent });
      setNotice("Data siswa berhasil disimpan.");
      await loadData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  }

  async function downloadExcelTemplate() {
    setError("");
    try {
      const response = await api.get(
        "/education/import/students/template",
        { responseType: "blob" }
      );
      downloadBlob(response.data, "template_data_siswa.xlsx");
    } catch (err) {
      setError(
        getErrorMessage(err) +
          " Gunakan template CSV sementara jika endpoint belum tersedia."
      );
    }
  }

  async function importExcel(event) {
    event.preventDefault();
    setError("");
    setNotice("");
    setImportResult(null);

    if (!file || !file.name.toLowerCase().endsWith(".xlsx")) {
      setError("Pilih file Excel berformat .xlsx.");
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError("Ukuran file maksimal 5 MB.");
      return;
    }

    setImporting(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post(
        "/education/import/students",
        formData,
        { timeout: 60000 }
      );

      const result = response.data;
      setImportResult(result);
      setNotice(
        `Impor selesai: ${result.imported ?? 0} berhasil, ` +
          `${result.failed ?? 0} gagal.`
      );
      setFile(null);

      const input = document.getElementById("education-excel-file");
      if (input) input.value = "";

      await loadData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setImporting(false);
    }
  }

  const schoolColumns = [
    { label: "Nama sekolah", key: "name" },
    { label: "NPSN", key: "npsn" },
    { label: "Jenjang", key: "school_level" },
    {
      label: "Status",
      render: (row) => (row.is_active ? "Aktif" : "Tidak aktif"),
    },
  ];

  const studentColumns = [
    { label: "Nomor siswa", key: "student_number" },
    { label: "Nama lengkap", key: "full_name" },
    { label: "ID sekolah", key: "school_id" },
    {
      label: "Status",
      render: (row) => (row.is_active ? "Aktif" : "Tidak aktif"),
    },
  ];

  const resultColumns = [
    { label: "Baris Excel", key: "row" },
    { label: "Nomor siswa", key: "student_number" },
    {
      label: "Status",
      render: (row) => (row.status === "imported" ? "Berhasil" : "Gagal"),
    },
    { label: "Keterangan", key: "message" },
  ];

  return (
    <div style={styles.page}>
      <header>
        <h2 style={{ margin: "0 0 8px" }}>Data Education</h2>
        <p style={{ margin: 0, color: "#667085" }}>
          Kelola data sekolah dan siswa MAI Nexus AI Education.
        </p>
      </header>

      <div style={styles.tabs}>
        <button
          type="button"
          style={{
            ...styles.secondary,
            ...(tab === "schools" ? styles.button : {}),
          }}
          onClick={() => {
            setTab("schools");
            setError("");
            setNotice("");
          }}
        >
          Data Sekolah ({schools.length})
        </button>
        <button
          type="button"
          style={{
            ...styles.secondary,
            ...(tab === "students" ? styles.button : {}),
          }}
          onClick={() => {
            setTab("students");
            setError("");
            setNotice("");
          }}
        >
          Data Siswa ({students.length})
        </button>
        <button
          type="button"
          style={styles.secondary}
          disabled={loading}
          onClick={loadData}
        >
          {loading ? "Memuat..." : "Muat ulang"}
        </button>
      </div>

      {error && (
        <div
          role="alert"
          style={{
            padding: 14,
            borderRadius: 8,
            background: "#fff1f0",
            color: "#a61b1b",
            overflowWrap: "anywhere",
          }}
        >
          {error}
        </div>
      )}

      {notice && (
        <div
          role="status"
          style={{
            padding: 14,
            borderRadius: 8,
            background: "#ecfdf3",
            color: "#166534",
          }}
        >
          {notice}
        </div>
      )}

      {tab === "schools" ? (
        <>
          <section style={styles.panel}>
            <h3>Tambah Sekolah</h3>
            <form onSubmit={createSchool} style={styles.form}>
              <Field label="Nama sekolah *">
                <input
                  style={styles.input}
                  value={schoolForm.name}
                  maxLength={200}
                  onChange={(e) => updateSchool("name", e.target.value)}
                  required
                />
              </Field>
              <Field label="NPSN">
                <input
                  style={styles.input}
                  value={schoolForm.npsn}
                  maxLength={20}
                  onChange={(e) => updateSchool("npsn", e.target.value)}
                />
              </Field>
              <Field label="Jenjang sekolah *">
                <select
                  style={styles.input}
                  value={schoolForm.school_level}
                  onChange={(e) => updateSchool("school_level", e.target.value)}
                  required
                >
                  {["PAUD", "TK", "SD", "SMP", "SMA", "SMK", "SLB", "MA", "Lainnya"].map(
                    (level) => (
                      <option key={level} value={level}>
                        {level}
                      </option>
                    )
                  )}
                </select>
              </Field>
              <Field label="Jenis sekolah *">
                <select
                  style={styles.input}
                  value={schoolForm.school_type}
                  onChange={(e) => updateSchool("school_type", e.target.value)}
                  required
                >
                  <option value="general">Umum</option>
                  <option value="islamic">Islam</option>
                  <option value="vocational">Kejuruan</option>
                  <option value="special_needs">Pendidikan khusus</option>
                  <option value="other">Lainnya</option>
                </select>
              </Field>
              <Field label="Alamat">
                <input
                  style={styles.input}
                  value={schoolForm.address}
                  maxLength={500}
                  onChange={(e) => updateSchool("address", e.target.value)}
                />
              </Field>
              <Field label="Status">
                <select
                  style={styles.input}
                  value={String(schoolForm.is_active)}
                  onChange={(e) =>
                    updateSchool("is_active", e.target.value === "true")
                  }
                >
                  <option value="true">Aktif</option>
                  <option value="false">Tidak aktif</option>
                </select>
              </Field>
              <div style={{ gridColumn: "1 / -1" }}>
                <button type="submit" style={styles.button} disabled={saving}>
                  {saving ? "Menyimpan..." : "Simpan Sekolah"}
                </button>
              </div>
            </form>
          </section>

          <section style={styles.panel}>
            <h3>Daftar Sekolah</h3>
            {loading ? (
              <p>Memuat data...</p>
            ) : (
              <Table
                columns={schoolColumns}
                rows={schools}
                emptyMessage="Belum ada data sekolah."
              />
            )}
          </section>
        </>
      ) : (
        <>
          <section style={styles.panel}>
            <h3>Tambah Siswa</h3>
            {schools.length === 0 ? (
              <p>Tambahkan sekolah terlebih dahulu.</p>
            ) : (
              <form onSubmit={createStudent} style={styles.form}>
                <Field label="Sekolah *">
                  <select
                    style={styles.input}
                    value={studentForm.school_id}
                    onChange={(e) => updateStudent("school_id", e.target.value)}
                    required
                  >
                    <option value="">Pilih sekolah</option>
                    {schools.map((school) => (
                      <option key={school.id} value={school.id}>
                        {school.name}
                      </option>
                    ))}
                  </select>
                </Field>
                <Field label="Nomor siswa *">
                  <input
                    style={styles.input}
                    value={studentForm.student_number}
                    maxLength={50}
                    onChange={(e) =>
                      updateStudent("student_number", e.target.value)
                    }
                    required
                  />
                </Field>
                <Field label="Nama lengkap *">
                  <input
                    style={styles.input}
                    value={studentForm.full_name}
                    maxLength={150}
                    onChange={(e) => updateStudent("full_name", e.target.value)}
                    required
                  />
                </Field>
                <Field label="Status">
                  <select
                    style={styles.input}
                    value={String(studentForm.is_active)}
                    onChange={(e) =>
                      updateStudent("is_active", e.target.value === "true")
                    }
                  >
                    <option value="true">Aktif</option>
                    <option value="false">Tidak aktif</option>
                  </select>
                </Field>
                <div style={{ gridColumn: "1 / -1" }}>
                  <button type="submit" style={styles.button} disabled={saving}>
                    {saving ? "Menyimpan..." : "Simpan Siswa"}
                  </button>
                </div>
              </form>
            )}
          </section>

          <section style={styles.panel}>
            <h3>Impor Siswa dari Excel</h3>
            <p style={{ color: "#667085", lineHeight: 1.6 }}>
              Isi template dengan kolom student_number, full_name, school_id,
              dan is_active. Maksimal 5 MB; batas backend 500 baris.
            </p>

            <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
              <button
                type="button"
                style={styles.secondary}
                onClick={downloadExcelTemplate}
                disabled={importing}
              >
                Unduh Template Excel
              </button>
              <button
                type="button"
                style={styles.secondary}
                onClick={downloadCsvTemplate}
                disabled={importing}
              >
                Unduh Template CSV
              </button>
            </div>

            <form
              onSubmit={importExcel}
              style={{ ...styles.form, marginTop: 16 }}
            >
              <Field label="Pilih file Excel (.xlsx) *">
                <input
                  id="education-excel-file"
                  type="file"
                  accept=".xlsx"
                  style={styles.input}
                  onChange={(e) => {
                    setFile(e.target.files?.[0] || null);
                    setImportResult(null);
                    setError("");
                  }}
                  required
                />
              </Field>
              <div style={{ display: "flex", alignItems: "flex-end" }}>
                <button
                  type="submit"
                  style={styles.button}
                  disabled={importing || !file}
                >
                  {importing ? "Mengimpor..." : "Unggah dan Impor"}
                </button>
              </div>
            </form>

            {importResult && (
              <div style={{ marginTop: 20 }}>
                <h4>Hasil Impor</h4>
                <p>
                  Total: {importResult.total_processed ?? 0} | Berhasil:{" "}
                  {importResult.imported ?? 0} | Gagal:{" "}
                  {importResult.failed ?? 0}
                </p>
                <Table
                  columns={resultColumns}
                  rows={importResult.results || []}
                  emptyMessage="Tidak ada rincian hasil."
                />
              </div>
            )}
          </section>

          <section style={styles.panel}>
            <h3>Daftar Siswa</h3>
            {loading ? (
              <p>Memuat data...</p>
            ) : (
              <Table
                columns={studentColumns}
                rows={students}
                emptyMessage="Belum ada data siswa."
              />
            )}
          </section>
        </>
      )}
    </div>
  );
}
