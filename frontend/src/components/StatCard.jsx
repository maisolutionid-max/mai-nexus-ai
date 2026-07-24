export default function StatCard({ title, value }) {
  return (
    <div
      style={{
        background: "#fff",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        marginBottom: "15px"
      }}
    >
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}
