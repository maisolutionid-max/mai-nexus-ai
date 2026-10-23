import React, { useState } from 'react';
import * as XLSX from 'xlsx';

export default function DataSiswa() {
  const [dataSiswa, setDataSiswa] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ nisn: '', nama: '', kelas: '' });

  // 1. Handle Upload File Excel
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
      const bstr = evt.target.result;
      const workbook = XLSX.read(bstr, { type: 'binary' });
      const wsname = workbook.SheetNames[0];
      const ws = workbook.Sheets[wsname];
      const parsedData = XLSX.utils.sheet_to_json(ws);

      setDataSiswa((prev) => [...prev, ...parsedData]);
      alert(`Berhasil mengimpor ${parsedData.length} data dari Excel!`);
    };
    reader.readAsBinaryString(file);
  };

  // 2. Handle Submit Input Manual
  const handleSubmitManual = (e) => {
    e.preventDefault();
    setDataSiswa((prev) => [...prev, formData]);
    setFormData({ nisn: '', nama: '', kelas: '' });
    setShowModal(false);
  };

  return (
    <div className="p-4 bg-slate-50 min-h-screen">
      <div className="flex flex-col gap-3 mb-6">
        <h1 className="text-lg font-bold text-slate-800">Manajemen Data Siswa</h1>
        
        {/* Tombol Aksi (Ramah Tampilan HP) */}
        <div className="grid grid-cols-2 gap-2">
          <button 
            onClick={() => setShowModal(true)}
            className="bg-blue-600 text-white py-2.5 px-3 rounded-lg text-sm font-medium shadow-sm hover:bg-blue-700"
          >
            + Tambah Manual
          </button>
          
          <label className="bg-emerald-600 text-white py-2.5 px-3 rounded-lg text-sm font-medium shadow-sm text-center cursor-pointer flex items-center justify-center">
            📁 Upload Excel
            <input 
              type="file" 
              accept=".xlsx, .xls, .csv" 
              onChange={handleFileUpload} 
              className="hidden" 
            />
          </label>
        </div>
      </div>

      {/* Tabel Data Responsif */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-x-auto">
        <table className="w-full text-left text-sm min-w-[320px]">
          <thead className="bg-slate-100 text-slate-700">
            <tr>
              <th className="p-3">NISN</th>
              <th className="p-3">Nama</th>
              <th className="p-3">Kelas</th>
            </tr>
          </thead>
          <tbody>
            {dataSiswa.length === 0 ? (
              <tr>
                <td colSpan="3" className="p-6 text-center text-slate-400">
                  Belum ada data tersimpan.
                </td>
              </tr>
            ) : (
              dataSiswa.map((item, index) => (
                <tr key={index} className="border-t border-slate-100">
                  <td className="p-3">{item.NISN || item.nisn}</td>
                  <td className="p-3">{item.Nama || item.nama}</td>
                  <td className="p-3">{item.Kelas || item.kelas}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Input Manual */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-end sm:items-center justify-center z-50 p-0 sm:p-4">
          <div className="bg-white w-full sm:max-w-md rounded-t-2xl sm:rounded-2xl p-5 shadow-lg">
            <div className="flex justify-between items-center mb-4 border-b pb-2">
              <h2 className="font-bold text-base">Form Tambah Siswa</h2>
              <button onClick={() => setShowModal(false)} className="text-slate-400 text-xl font-bold">&times;</button>
            </div>
            
            <form onSubmit={handleSubmitManual} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold mb-1 text-slate-600">NISN</label>
                <input 
                  type="text" 
                  required
                  className="w-full border border-slate-300 p-2.5 rounded-lg text-sm"
                  value={formData.nisn}
                  onChange={(e) => setFormData({ ...formData, nisn: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-xs font-semibold mb-1 text-slate-600">NAMA LENGKAP</label>
                <input 
                  type="text" 
                  required
                  className="w-full border border-slate-300 p-2.5 rounded-lg text-sm"
                  value={formData.nama}
                  onChange={(e) => setFormData({ ...formData, nama: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-xs font-semibold mb-1 text-slate-600">KELAS</label>
                <input 
                  type="text" 
                  required
                  className="w-full border border-slate-300 p-2.5 rounded-lg text-sm"
                  value={formData.kelas}
                  onChange={(e) => setFormData({ ...formData, kelas: e.target.value })}
                />
              </div>
              <div className="flex gap-2 pt-3">
                <button 
                  type="button" 
                  onClick={() => setShowModal(false)}
                  className="w-1/2 bg-slate-100 text-slate-600 py-2.5 rounded-lg text-sm font-medium"
                >
                  Batal
                </button>
                <button 
                  type="submit" 
                  className="w-1/2 bg-blue-600 text-white py-2.5 rounded-lg text-sm font-medium"
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
