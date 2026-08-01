import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {

  const location = useLocation();

  const menus = [
    { name: "Dashboard", path: "/dashboard", icon: "🏠" },
    { name: "Customer", path: "/customer", icon: "👥" },
    { name: "Product", path: "/product", icon: "📦" },
    { name: "Order", path: "/order", icon: "📝" },
    { name: "Transaction", path: "/transaction", icon: "💳" },
    { name: "Payment", path: "/payment", icon: "💰" },
    { name: "Report", path: "/report", icon: "📊" },
    { name: "AI Insight", path: "/ai", icon: "🤖" },
  ];

  return (
    <div
      style={{
        width: "250px",
        background: "#1e293b",
        color: "#fff",
        minHeight: "100vh",
        padding: "20px",
      }}
    >
      <h2
        style={{
          textAlign: "center",
          marginBottom: "30px",
          color: "#60a5fa",
        }}
      >
        Mai Nexus AI
      </h2>

      {menus.map((menu) => (
        <Link
          key={menu.path}
          to={menu.path}
          style={{
            display: "block",
            textDecoration: "none",
            color:
              location.pathname === menu.path
                ? "#38bdf8"
                : "#ffffff",
            padding: "12px",
            borderRadius: "8px",
            marginBottom: "8px",
            background:
              location.pathname === menu.path
                ? "#334155"
                : "transparent",
          }}
        >
          {menu.icon} {menu.name}
        </Link>
      ))}

      <div style={{ marginTop: "40px" }}>
        <Link
          to="/login"
          style={{
            textDecoration: "none",
            color: "#f87171",
            fontWeight: "bold",
          }}
        >
          🚪 Logout
        </Link>
      </div>
    </div>
  );
}
