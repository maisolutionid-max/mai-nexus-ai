import MainLayout from "../layouts/MainLayout";

export default function Dashboard() {

  return (
    <MainLayout>

      <h1
        style={{
          marginBottom: "25px",
          color: "#1e293b",
        }}
      >
        Dashboard
      </h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: "20px",
          marginBottom: "30px",
        }}
      >

        <Card
          title="Customer"
          value="1,250"
          color="#2563eb"
        />

        <Card
          title="Order"
          value="326"
          color="#16a34a"
        />

        <Card
          title="Revenue"
          value="Rp 1,250 M"
          color="#ea580c"
        />

        <Card
          title="Payment"
          value="98%"
          color="#9333ea"
        />

      </div>

      <div
        style={{
          background:"#ffffff",
          padding:"25px",
          borderRadius:"12px",
          boxShadow:"0 2px 8px rgba(0,0,0,.08)"
        }}
      >

        <h2>🤖 Mai AI Business Insight</h2>

        <hr />

        <p>
          Revenue meningkat
          <strong> 15%</strong>
          dibanding bulan lalu.
        </p>

        <p>
          Customer baru bertambah
          <strong> 38</strong>.
        </p>

        <p>
          Produk terlaris:
          <strong> Laundry Express</strong>.
        </p>

        <p>
          Prediksi omzet minggu depan:
          <strong> +12%</strong>.
        </p>

      </div>
<div
  style={{
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "20px",
    marginTop: "25px",
  }}
>
  <div
    style={{
      background: "#ffffff",
      borderRadius: "12px",
      padding: "20px",
      boxShadow: "0 2px 8px rgba(0,0,0,.08)",
    }}
  >
    <h2>📈 Revenue Trend</h2>

    <div
      style={{
        height: "250px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        color: "#888",
        border: "2px dashed #ddd",
        borderRadius: "10px",
      }}
    >
      Revenue Chart (Coming Soon)
    </div>
  </div>

  <div
    style={{
      background: "#ffffff",
      borderRadius: "12px",
      padding: "20px",
      boxShadow: "0 2px 8px rgba(0,0,0,.08)",
    }}
  >
    <h2>🏆 Top Product</h2>

    <p>🥇 Laundry Express</p>
    <p>🥈 Dry Cleaning</p>
    <p>🥉 Cuci Sepatu</p>

    <hr />

    <h2>👥 Top Customer</h2>

    <p>PT ABC</p>
    <p>PT XYZ</p>
    <p>CV Maju Jaya</p>
  </div>
</div>
    </MainLayout>
  );

}

function Card({ title, value, color }){

    return(

        <div
            style={{
                background:"#fff",
                padding:"20px",
                borderRadius:"12px",
                borderLeft:`6px solid ${color}`,
                boxShadow:"0 2px 8px rgba(0,0,0,.08)"
            }}
        >

            <h3>{title}</h3>

            <h1
                style={{
                    color:color,
                    marginTop:"15px"
                }}
            >
                {value}
            </h1>

        </div>

    );

               }
