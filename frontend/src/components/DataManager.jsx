import React, { useState } from 'react';
import * as XLSX from 'xlsx';

export default function DataManager({ title, fields, initialData = [] }) {
  const [dataList, setDataList] = useState(initialData);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({});

  // Reset form berdasarkan kolom aktif
  const handleOpenModal = () => {
    const emptyForm = {};
    fields.forEach((f) => (emptyForm[f.key] = ''));
    setFormData(emptyForm);
    setShowModal(true);
  };

  // Upload & Baca File Excel (.xlsx / .csv)
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const bstr = evt.target.result;
        const workbook = XLSX.read(bstr, { type: 'binary' });
        const wsname = workbook.SheetNames[0];
        const ws = workbook.Sheets[wsname];
        const parsedData = XLSX.utils.sheet_to_json(ws);
        
        setDataList((prev) => [...prev, ...parsedData]);
        alert(`Berhasil mengimpor ${parsedData.length} data!`);
      } catch (err) {
        alert('Gagal membaca file Excel. Pastikan format file sesuai.');
      }
    };
    reader.readAsBinaryString(file);
    e.target.value = ''; // Reset input file
  };

  // Submit Input Manual
  const handleManualSubmit = (e) => {
    e.preventDefault();
    setDataList((prev) => [...prev, formData]);
    setShowModal(false);
  };

  return (
    <div style={{ padding: '16px', fontFamily: 'sans-serif' }}>
      {/* Header & Tombol Aksi */}
      <div style={{ marginBottom: '20px', display: 'flex', flexWrap: 'wrap', gap: '10px', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 'bold', margin: 0, color: '#1e293b' }}>
          Manajemen {title}
        </h2>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            onClick={handleOpenModal}
            style={{
              backgroundColor: '#2563eb',
              color: '#ffffff',
              padding: '10px 16px',
              borderRadius: '8px',
              border: 'none',
              fontWeight: '600',
              fontSize: '13px',
              cursor: 'pointer'
            }}
          >
            + Tambah Manual
          </button>

          <label style={{
            backgroundColor: '#059669',
            color: '#ffffff',
            padding: '10px 16px',
            borderRadius: '8px',
            fontWeight: '600',
            fontSize: '13px',
            cursor: 'pointer',
            display: 'inline-block'
          }}>
            📁 Upload Excel
            <input 
              type="file" 
              accept=".xlsx, .xls, .csv" 
              onChange={handleFileUpload} 
              style={{ display: 'none' }} 
            />
          </label>
        </div>
      </div>

      {/* Tabel Data Rapi */}
      <div style={{ backgroundColor: '#ffffff', borderRadius: '12px', border: '1px solid #e2e8f0', overflowX: 'auto', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
          <thead>
            <tr style={{ backgroundColor: '#f8fafc', borderBottom: '1px solid #e2e8f0', color: '#475569' }}>
              {fields.map((col) => (
                <th key={col.key} style={{ padding: '12px 16px', fontWeight: '600' }}>{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {dataList.length === 0 ? (
              <tr>
                <td colSpan={fields.length} style={{ padding: '24px', textAlign: 'center', color: '#94a3b8' }}>
                  Belum ada data {title.toLowerCase()}. Silakan tambah manual atau upload file Excel.
                </td>
              </tr>
            ) : (
              dataList.map((item, index) => (
                <tr key={index} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  {fields.map((col) => (
                    <td key={col.key} style={{ padding: '12px 16px', color: '#334155' }}>
                      {item[col.key] || item[col.label] || '-'}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Popup (Bottom Sheet HP / Dialog) */}
      {showModal && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          padding: '16px'
        }}>
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '16px',
            width: '100%',
            maxWidth: '450px',
            padding: '20px',
            boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid #f1f5f9', paddingBottom: '10px' }}>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 'bold', color: '#0f172a' }}>Form Input {title}</h3>
              <button 
                onClick={() => setShowModal(false)}
                style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer', color: '#94a3b8' }}
              >
                &times;
              </button>
            </div>

            <form onSubmit={handleManualSubmit}>
              {fields.map((field) => (
                <div key={field.key} style={{ marginBottom: '14px' }}>
                  <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: '#475569', marginBottom: '6px' }}>
                    {field.label.toUpperCase()}
                  </label>
                  <input 
                    type="text" 
                    required
                    placeholder={`Masukkan ${field.label}`}
                    style={{
                      width: '100%',
                      padding: '10px 12px',
                      borderRadius: '8px',
                      border: '1px solid #cbd5e1',
                      fontSize: '14px',
                      boxSizing: 'border-box'
                    }}
                    value={formData[field.key] || ''}
                    onChange={(e) => setFormData({ ...formData, [field.key]: e.target.value })}
                  />
                </div>
              ))}

              <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                <button 
                  type="button" 
                  onClick={() => setShowModal(false)}
                  style={{
                    flex: 1,
                    padding: '10px',
                    borderRadius: '8px',
                    border: '1px solid #cbd5e1',
                    backgroundColor: '#f8fafc',
                    color: '#475569',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  Batal
                </button>
                <button 
                  type="submit" 
                  style={{
                    flex: 1,
                    padding: '10px',
                    borderRadius: '8px',
                    border: 'none',
                    backgroundColor: '#2563eb',
                    color: '#ffffff',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  Simpan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
