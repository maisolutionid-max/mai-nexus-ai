export default function Navbar() {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "15px 25px",
        borderRadius: "10px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "20px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div>
        <h2 style={{ margin: 0 }}>Mai Nexus AI</h2>
        <small>AI Business Operating System</small>
      </div>

      <div
        style={{
          display: "flex",
          gap: "15px",
          alignItems: "center",
        }}
      >
        <span>🔔</span>
        <span>👤 Admin</span>
      </div>
    </div>
  );
}
