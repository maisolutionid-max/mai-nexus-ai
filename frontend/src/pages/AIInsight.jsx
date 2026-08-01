import MainLayout from "../layouts/MainLayout";
import PageHeader from "../components/PageHeader";

export default function AIInsight() {

  return (

    <MainLayout>

      <PageHeader
        title="Mai AI Insight"
        subtitle="AI Business Operating System"
      />

      <div
        style={{
          background: "#fff",
          padding: "25px",
          borderRadius: "12px",
          boxShadow: "0 2px 10px rgba(0,0,0,.08)"
        }}
      >

        <h2>🤖 AI Business Insight</h2>

        <hr />

        <p>📈 Revenue meningkat <b>15%</b> dibanding bulan lalu.</p>

        <p>👥 Customer baru bertambah <b>38</b>.</p>

        <p>📦 Produk terlaris adalah <b>Laundry Express</b>.</p>

        <p>📝 Order selesai mencapai <b>96%</b>.</p>

        <p>💰 Tingkat pembayaran berhasil <b>98%</b>.</p>

        <p>📊 Prediksi omzet minggu depan <b>+12%</b>.</p>

        <div
          style={{
            marginTop: "30px",
            padding: "20px",
            background: "#eff6ff",
            borderRadius: "10px",
            borderLeft: "5px solid #2563eb"
          }}
        >

          <h3>💡 Rekomendasi Mai AI</h3>

          <ul>
            <li>Fokus promosi Laundry Express.</li>
            <li>Hubungi kembali customer yang tidak aktif lebih dari 30 hari.</li>
            <li>Tingkatkan promosi digital pada akhir pekan.</li>
            <li>Optimalkan kapasitas produksi pada jam sibuk.</li>
          </ul>

        </div>

      </div>

    </MainLayout>

  );

}
