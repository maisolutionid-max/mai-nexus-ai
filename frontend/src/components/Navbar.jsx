export default function Navbar() {

  return (

    <div
      style={{
        background: "#ffffff",
        padding: "15px 25px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        boxShadow: "0 2px 8px rgba(0,0,0,.08)"
      }}
    >

      <div>

        <h2
          style={{
            margin:0
          }}
        >
          🚀 Mai Nexus AI
        </h2>

        <small
          style={{
            color:"#666"
          }}
        >
          AI Business Operating System
        </small>

      </div>

      <div
        style={{
          display:"flex",
          alignItems:"center",
          gap:"20px"
        }}
      >

        <input
          placeholder="Search..."
          style={{
            padding:"8px 12px",
            borderRadius:"8px",
            border:"1px solid #ddd",
            width:"220px"
          }}
        />

        <span>🔔</span>

        <span>⚙️</span>

        <span>👤 Admin</span>

      </div>

    </div>

  );

}
