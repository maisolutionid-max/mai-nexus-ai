import MainLayout from "../layouts/MainLayout";
import PageHeader from "../components/PageHeader";
import StatCard from "../components/StatCard";

export default function Report() {

  return (
    <MainLayout>

      <PageHeader
        title="Business Report"
        subtitle="Business Performance Summary"
      />

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: "20px",
        }}
      >

        <StatCard
          title="Revenue"
          value="Rp 1.250 M"
          color="#16a34a"
        />

        <StatCard
          title="Customer"
          value="1.250"
          color="#2563eb"
        />

        <StatCard
          title="Order"
          value="326"
          color="#ea580c"
        />

        <StatCard
          title="Payment"
          value="98%"
          color="#9333ea"
        />

      </div>

      <div
        style={{
          marginTop: "30px",
          background: "#fff",
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 2px 10px rgba(0,0,0,.08)"
        }}
      >

        <h2>Business Summary</h2>

        <hr />

        <p>Revenue bulan ini meningkat <b>15%</b>.</p>

        <p>Customer baru bertambah <b>38</b>.</p>

        <p>Order selesai <b>312</b>.</p>

        <p>Payment Success Rate <b>98%</b>.</p>

      </div>

    </MainLayout>
  );

}
