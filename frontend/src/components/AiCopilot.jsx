import React, { useState } from "react";

export default function AiCopilot() {
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Halo! Saya MAI Nexus AI Teacher Copilot. Ada yang bisa saya bantu hari ini? Anda bisa meminta saya membuat RPP, menyusun soal kuis, atau membuat analisis pembelajaran.",
    },
  ]);
  const [inputPrompt, setInputPrompt] = useState("");
  const [isThinking, setIsThinking] = useState(false);

  // Template prompt cepat
  const quickPrompts = [
    "Buatkan RPP Matematika Kelas 7 materi Persamaan Linear",
    "Buat 5 soal pilihan ganda Fisika SMA tentang Hukum Newton",
    "Buatkan draf surat pemberitahuan kegiatan outing class",
  ];

  const handleSend = (textToSend) => {
    const prompt = textToSend || inputPrompt;
    if (!prompt.trim()) return;

    // Tambah pesan pengguna
    const newMessages = [...messages, { sender: "user", text: prompt }];
    setMessages(newMessages);
    if (!textToSend) setInputPrompt("");
    setIsThinking(true);

    // Simulasi respons AI Copilot (akan dihubungkan ke API AI nantinya)
    setTimeout(() => {
      let aiResponse = "";
      if (prompt.toLowerCase().includes("rpp")) {
        aiResponse = `**DRAF RENCANA PELAKSANAAN PEMBELAJARAN (RPP)**\n\n- **Mata Pelajaran:** Matematika\n- **Materi:** Persamaan Linear Satu Variabel\n- **Alokasi Waktu:** 2 x 45 Menit\n\n**Tujuan Pembelajaran:**\n1. Memahami konsep variabel dan konstanta.\n2. Menyelesaikan persamaan linear sederhana.\n\n**Kegiatan Pembelajaran:**\n1. Pendahuluan (10 menit): Apersepsi materi.\n2. Inti (70 menit): Diskusi kelompok dan latihan soal.\n3. Penutup (10 menit): Kesimpulan dan refleksi.`;
      } else if (prompt.toLowerCase().includes("soal")) {
        aiResponse = `**DRAF SOAL EVALUASI**\n\n1. Sebuah benda bermassa 2 kg didorong dengan gaya 10 N. Berapakah percepatan benda tersebut?\n   a. 2 m/s²\n   b. 5 m/s²\n   c. 10 m/s²\n   d. 20 m/s²\n   *Kunci Jawaban: B (F = m . a -> a = 10/2 = 5)*`;
      } else {
        aiResponse = `Tentu, saya siap membantu terkait "${prompt}". Sebagai asisten AI Edukasi MAI Nexus, saya dapat menyesuaikan format ini sesuai standar kurikulum sekolah Anda. Apakah ada detail tambahan yang ingin disesuaikan?`;
      }

      setMessages([...newMessages, { sender: "ai", text: aiResponse }]);
      setIsThinking(false);
    }, 1200);
  };

  return (
    <div style={{ padding: "16px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
        <span style={{ fontSize: "24px" }}>🤖</span>
        <div>
          <h2 style={{ fontSize: "18px", fontWeight: "bold", margin: 0, color: "#1e293b" }}>
            AI Teacher Copilot
          </h2>
          <p style={{ fontSize: "12px", color: "#64748b", margin: 0 }}>
            Asisten cerdas pembuatan modul ajar, soal, dan administrasi guru.
          </p>
        </div>
      </div>

      {/* Area Output Chat */}
      <div
        style={{
          backgroundColor: "#ffffff",
          borderRadius: "12px",
          border: "1px solid #e2e8f0",
          padding: "16px",
          height: "380px",
          overflowY: "auto",
          marginBottom: "16px",
          display: "flex",
          flexDirection: "column",
          gap: "12px",
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              backgroundColor: msg.sender === "user" ? "#2563eb" : "#f1f5f9",
              color: msg.sender === "user" ? "#ffffff" : "#1e293b",
              padding: "12px 16px",
              borderRadius: "12px",
              maxWidth: "85%",
              fontSize: "13px",
              lineHeight: "1.5",
              whiteSpace: "pre-line",
            }}
          >
            {msg.text}
          </div>
        ))}
        {isThinking && (
          <div
            style={{
              alignSelf: "flex-start",
              backgroundColor: "#f1f5f9",
              color: "#64748b",
              padding: "10px 14px",
              borderRadius: "12px",
              fontSize: "12px",
              fontStyle: "italic",
            }}
          >
            ⚡ MAI Nexus AI sedang berpikir dan merancang teks...
          </div>
        )}
      </div>

      {/* Akses Cepat Prompt */}
      <div style={{ marginBottom: "12px", display: "flex", gap: "8px", overflowX: "auto", pb: "4px" }}>
        {quickPrompts.map((p, i) => (
          <button
            key={i}
            onClick={() => handleSend(p)}
            style={{
              backgroundColor: "#f8fafc",
              border: "1px solid #cbd5e1",
              borderRadius: "20px",
              padding: "6px 12px",
              fontSize: "11px",
              color: "#475569",
              whiteSpace: "nowrap",
              cursor: "pointer",
            }}
          >
            ✨ {p}
          </button>
        ))}
      </div>

      {/* Input Box */}
      <div style={{ display: "flex", gap: "8px" }}>
        <input
          type="text"
          placeholder="Tanyakan atau minta AI buatkan modul/soal..."
          value={inputPrompt}
          onChange={(e) => setInputPrompt(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          style={{
            flex: 1,
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
            fontSize: "13px",
            boxSizing: "border-box",
          }}
        />
        <button
          onClick={() => handleSend()}
          style={{
            backgroundColor: "#2563eb",
            color: "#ffffff",
            border: "none",
            borderRadius: "8px",
            padding: "0 18px",
            fontWeight: "bold",
            fontSize: "13px",
            cursor: "pointer",
          }}
        >
          Kirim
        </button>
      </div>
    </div>
  );
}
