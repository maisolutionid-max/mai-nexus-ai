export default function MainLayout({ children }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside
        style={{
          width: "250px",
          background: "#1E3A8A",
          color: "white",
          padding: "20px"
        }}
      >
        <h2>MAI Nexus AI</h2>
        <hr />
        <p>📊 Dashboard</p>
        <p>👥 Customer</p>
        <p>📦 Order</p>
        <p>🤖 AI Agent</p>
        <p>⚙️ Settings</p>
      </aside>

      <main
        style={{
          flex: 1,
          padding: "30px",
          background: "#F8FAFC"
        }}
      >
        {children}
      </main>
    </div>
  );
}
