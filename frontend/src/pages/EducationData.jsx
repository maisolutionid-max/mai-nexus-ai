
import React, { useCallback, useEffect, useState } from "react";
import api from "../services/api";

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

const excelHeaders = [
  "student_number",
  "full_name",
  "school_id",
  "is_active",
];

const styles = {
  page: {
    display: "grid",
    gap: 20,
    color: "var(--text-primary, #172033)",
  },
  tabs: {
    display: "flex",
    flexWrap: "wrap",
    gap: 8,
  },
  tab: {
    padding: "10px 16px",
    border: "1px solid #d9dfeb",
    borderRadius: 10,
    background: "#fff",
    color: "#172033",
    cursor: "pointer",
    fontWeight: 600,
  },
  activeTab: {
    background: "#14213d",
    color: "#fff",
    borderColor: "#14213d",
  },
  panel: {
    background: "#fff",
    border: "1px solid #e1e6ef",
    borderRadius: 14,
    padding: 20,
    minWidth: 0,
  },
  form: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: 16,
  },
  field: {
    display: "grid",
    gap: 7,
    minWidth: 0,
  },
  label: {
    fontSize: 14,
    fontWeight: 600,
  },
  input: {
    width: "100%",
    minWidth: 0,
    boxSizing: "border-box",
    padding: "11px 12px",
    border: "1px solid #ccd4e1",
    borderRadius: 8,
    background: "#fff",
    color: "#172033",
    font: "inherit",
  },
  button: {
    border: 0,
    borderRadius: 8,
    padding: "11px 16px",
    background: "#14213d",
    color: "#fff",
    fontWeight: 600,
    cursor: "pointer",
  },
  secondaryButton: {
    border: "1px solid #ccd4e1",
    borderRadius: 8,
    padding: "10px 14px",
    background: "#fff",
    color: "#172033",
    cursor: "pointer",
  },
  tableWrap: {
    width: "100%",
    overflowX: "auto",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    minWidth: 520,
  },
  cell: {
    padding: "12px 10px",
    textAlign: "left",
    borderBottom: "1px solid #edf0f5",
    fontSize: 14,
  },
};

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
    return "Backend belum dapat dihubungi. Periksa koneksi dan URL API.";
  }

  if (error.response.status === 401) {
    return "Sesi login tidak tersedia atau sudah berakhir.";
  }

  if (error.response.status === 403) {
    return "Akun belum memiliki izin untuk mengakses data Education.";
  }

  return `Permintaan gagal (${error.response.status}). Periksa data dan coba kembali.`;
}

function normalizeList(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.items)) return data.items;
  if (Array.isArray(data?.data)) return data.data;
  return [];
}

function Field({ label, children }) {
  return (
    <label style={styles.field}>
      <span style={styles.label}>{label}</span>
      {children}
    </label>
  );
}

function downloadBlob(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();

  window.setTimeout(() => window.URL.revokeObjectURL(url), 1000);
}

function downloadCsvTemplate() {
  const rows = [
    excelHeaders,
    ["S-0001", "Nama Contoh", "1", "TRUE"],
  ];

  const csv = rows
    .map((row) =>
      row
        .map((value) => `"${String(value).replace(/"/g, '""')}"`)
        .join(",")
    )
    .join("\r\n");

  const blob = new Blob(["\uFEFF" + csv], {
    type: "text/csv;charset=utf-8;",
  });

  downloadBlob(blob, "template_data_siswa.csv");
}

export default function EducationData() {
  const [activeTab, setActiveTab] = useState("schools");
  const [schools, setSchools] = useState([]);
  const [students, setStudents] = useState([]);
  const [schoolForm, setSchoolForm] = useState(initialSchool);
  const [studentForm, setStudentForm] = useState(initialStudent);
  const [excelFile, setExcelFile] = useState(null);
  const [importResults, setImportResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const loadData = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const [schoolResponse, studentResponse] = await Promise.all([
        api.get("/education/schools"),
        api.get("/education/students"),
      ]);

      setSchools(normalizeList(schoolResponse.data));
      setStudents(normalizeList(studentResponse.data));
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  function updateSchool(field, value) {
    setSchoolForm((previous) => ({ ...previous, [field]: value }));
  }

  function updateStudent(field, value) {
    setStudentForm((previous) => ({ ...previous, [field]: value }));
  }

  async function handleCreateSchool(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setNotice("");

    const payload = {
      name: schoolForm.name.trim(),
      npsn: schoolForm.npsn.trim() || null,
      school_level: schoolForm.school_level,
      school_type: schoolForm.school_type,
      address: schoolForm.address.trim() || null,
      is_active: schoolForm.is_active,
    };

    try {
      await api.post("/education/schools", payload);
      setSchoolForm(initialSchool);
      setNotice("Data sekolah berhasil disimpan.");
      await loadData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  }

  async function handleCreateStudent(event) {
    event.preventDefault();
    setSaving(true);
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
      setError("Nomor siswa, nama lengkap, dan sekolah wajib diisi.");
      setSaving(false);
      return;
    }

    try {
      await api.post("/education/students", payload);
      setStudentForm(initialStudent);
      setNotice("Data siswa berhasil disimpan.");
      await loadData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  }

  async function handleDownloadTemplate() {
    setError("");
    setNotice("");

    try {
      const response = await api.get(
        "/education/import/students/template",
        { responseType: "blob" }
      );

      downloadBlob(response.data, "template_data_siswa.xlsx");
    } catch (err) {
      setError(
        getErrorMessage(err) +
          " Jika endpoint template belum tersedia, gunakan template CSV sementara."
      );
    }
  }

  async function handleImportExcel(event) {
    event.preventDefault();

    if (!excelFile) {
      setError("Pilih file Excel terlebih dahulu.");
      return;
    }

    if (!excelFile.name.toLowerCase().endsWith(".xlsx")) {
      setError("Pilih file dengan format .xlsx.");
      return;
    }

    if (excelFile.size > 5 * 1024 * 1024) {
      setError("Ukuran file maksimal 5 MB.");
      return;
    }

    setImporting(true);
    setError("");
    setNotice("");
    setImportResults(null);

    try {
      const formData = new FormData();
      formData.append("file", excelFile);

      const response = await api.post(
        "/education/import/students",
        formData,
        { timeout: 60000 }
      );

      setImportResults(response.data);
      setNotice(
        `Impor selesai: ${response.data.imported ?? 0} berhasil, ` +
          `${response.data.failed ?? 0} gagal.`
      );
      setExcelFile(null);

      const fileInput = document.getElementById("education-excel-file");
      if (fileInput) fileInput.value = "";

      await loadData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setImporting(false);
    }
  }

  return (
    <div style={styles.page}>
      <div>
        <h2 style={{ margin: "0 0 8px" }}>Data Education</h2>
        <p style={{ margin: 0, color: "#667085", lineHeight: 1.6 }}>
          Kelola data sekolah dan siswa melalui MAI Nexus AI Education.
        </p>
      </div>

      <div style={styles.tabs}>
        <button
          type="button"
          style={{
            ...styles.tab,
            ...(activeTab === "schools" ? styles.activeTab : {}),
          }}
          onClick={() => {
            setActiveTab("schools");
            setError("");
            setNotice("");
          }}
        >
          Data Sekolah ({schools.length})
        </button>

        <button
          type="button"
          style={{
            ...styles.tab,
            ...(activeTab === "students" ? styles.activeTab : {}),
          }}
          onClick={() => {
            setActiveTab("students");
            setError("");
            setNotice("");
          }}
        >
          Data Siswa ({students.length})
        </button>

        <button
          type="button"
          style={styles.secondaryButton}
          onClick={loadData}
          disabled={loading}
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

      {activeTab === "schools" ? (
        <>
          <section style={styles.panel}>
            <h3 style={{ marginTop: 0 }}>Tambah Sekolah</h3>

            <form onSubmit={handleCreateSchool} style={styles.form}>
              <Field label="Nama sekolah *">
                <input
                  style={styles.input}
                  value={schoolForm.name}
                  onChange={(event) => updateSchool("name", event.target.value)}
                  maxLength={200}
                  required
                />
              </Field>

              <Field label="NPSN">
                <input
                  style={styles.input}
                  value={schoolForm.npsn}
                  onChange={(event) => updateSchool("npsn", event.target.value)}
                  maxLength={20}
                />
              </Field>

              <Field label="Jenjang sekolah *">
                <select
                  style={styles.input}
                  value={schoolForm.school_level}
                  onChange={(event) =>
                    updateSchool("school_level", event.target.value)
                  }
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
                  onChange={(event) =>
                    updateSchool("school_type", event.target.value)
                  }
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
                  onChange={(event) =>
                    updateSchool("address", event.target.value)
                  }
                  maxLength={500}
                />
              </Field>

              <Field label="Status">
                <select
                  style={styles.input}
                  value={String(schoolForm.is_active)}
                  onChange={(event) =>
                    updateSchool("is_active", event.target.value === "true")
                  }
                >
                  <option value="true">Aktif</option>
                  <option value="false">Tidak aktif</option>
                </select>
              </Field>

              <div style={{ gridColumn: "1 / -1", textAlign: "right" }}>
                <button style={styles.button} disabled={saving} type="submit">
                  {saving ? "Menyimpan..." : "Simpan Sekolah"}
                </button>
              </div>
            </form>
          </section>

          <section style={styles.panel}>
            <h3 style={{ marginTop: 0 }}>Daftar Sekolah</h3>

            {loading ? (
              <p>Memuat data sekolah...</p>
            ) : schools.length === 0 ? (
              <p style={{ color: "#667085" }}>
                Belum ada data sekolah, atau backend belum terhubung.
              </p>
            ) : (
              <div style={styles.tableWrap}>
                <table style={styles.table}>
                  <thead>
                    <tr>
                      {["Nama sekolah", "NPSN", "Jenjang", "Status"].map(
                        (heading) => (
                          <th key={heading} style={styles.cell}>
                            {heading}
                          </th>
                        )
                      )}
                    </tr>
                  </thead>
                  <tbody>
                    {schools.map((school) => (
                      <tr key={school.id}>
                        <td style={styles.cell}>{school.name}</td>
                        <td style={styles.cell}>{school.npsn || "—"}</td>
                        <td style={styles.cell}>{school.school_level}</td>
                        <td style={styles.cell}>
                          {school.is_active ? "Aktif" : "Tidak aktif"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      ) : (
        <>
          <section style={styles.panel}>
            <h3 style={{ marginTop: 0 }}>Tambah Siswa</h3>

            {schools.length === 0 ? (
              <p style={{ color: "#667085" }}>
                Tambahkan sekolah terlebih dahulu sebelum memasukkan siswa.
              </p>
            ) : (
              <form onSubmit={handleCreateStudent} style={styles.form}>
                <Field label="Sekolah *">
                  <select
                    style={styles.input}
                    value={studentForm.school_id}
                    onChange={(event) =>
                      updateStudent("school_id", event.target.value)
                    }
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
                    onChange={(event) =>
                      updateStudent("student_number", event.target.value)
                    }
                    maxLength={50}
                    required
                  />
                </Field>

                <Field label="Nama lengkap *">
                  <input
                    style={styles.input}
                    value={studentForm.full_name}
                    onChange={(event) =>
                      updateStudent("full_name", event.target.value)
                    }
                    maxLength={150}
                    required
                  />
                </Field>

                <Field label="Status">
                  <select
                    style={styles.input}
                    value={String(studentForm.is_active)}
                    onChange={(event) =>
                      updateStudent("is_active", event.target.value === "true")
                    }
                  >
                    <option value="true">Aktif</option>
                    <option value="false">Tidak aktif</option>
                  </select>
                </Field>

                <div style={{ gridColumn: "1 / -1", textAlign: "right" }}>
                  <button style={styles.button} disabled={saving} type="submit">
                    {saving ? "Menyimpan..." : "Simpan Siswa"}
                  </button>
                </div>
              </form>
            )}
          </section>

          <section style={styles.panel}>
            <h3 style={{ marginTop: 0 }}>Impor Siswa dari Excel</h3>

            <p style={{ color: "#667085", lineHeight: 1.6 }}>
              Unduh template Excel, isi data siswa, kemudian unggah kembali.
              Maksimal 500 baris data dan ukuran file 5 MB.
            </p>
                <button
                  type="submit"
                  style={styles.button}
                  disabled={importing || !excelFile}
                >
                  {importing ? "Mengimpor..." : "Unggah dan Impor"}
                </button>
              </div>
            </form>

            <p style={{ fontSize: 13, color: "#667085", lineHeight: 1.6 }}>
              Kolom: student_number, full_name, school_id, is_active.
              Gunakan ID sekolah yang terdaftar pada akun/tenant terkait.
            </p>

            {importResults && (
              <div style={{ marginTop: 20 }}>
                <h4>Hasil Impor</h4>
                <p>
                  Total diproses: {importResults.total_processed ?? 0} |
                  Berhasil: {importResults.imported ?? 0} |
                  Gagal: {importResults.failed ?? 0}
                </p>

                <div style={styles.tableWrap}>
                  <table style={styles.table}>
                    <thead>
                      <tr>
                        {[
                          "Baris Excel",
                          "Nomor siswa",
                          "Status",
                          "Keterangan",
                        ].map((heading) => (
                          <th key={heading} style={styles.cell}>
                            {heading}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {(importResults.results || []).map((item, index) => (
                        <tr key={`${item.row}-${index}`}>
                          <td style={styles.cell}>{item.row}</td>
                          <td style={styles.cell}>
                            {item.student_number || "—"}
                          </td>
                          <td style={styles.cell}>
                            {item.status === "imported" ? "Berhasil" : "Gagal"}
                          </td>
                          <td style={styles.cell}>{item.message}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </section>

          <section style={styles.panel}>
            <h3 style={{ marginTop: 0 }}>Daftar Siswa</h3>

            {loading ? (
              <p>Memuat data siswa...</p>
            ) : students.length === 0 ? (
              <p style={{ color: "#667085" }}>Belum ada data siswa.</p>
            ) : (
              <div style={styles.tableWrap}>
                <table style={styles.table}>
                  <thead>
                    <tr>
                      {[
                        "Nomor siswa",
                        "Nama lengkap",
                        "ID sekolah",
                        "Status",
                      ].map((heading) => (
                        <th key={heading} style={styles.cell}>
                          {heading}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {students.map((student) => (
                      <tr key={student.id}>
                        <td style={styles.cell}>{student.student_number}</td>
                        <td style={styles.cell}>{student.full_name}</td>
                        <td style={styles.cell}>{student.school_id}</td>
                        <td style={styles.cell}>
                          {student.is_active ? "Aktif" : "Tidak aktif"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
