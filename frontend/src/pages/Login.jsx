import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const handleLogin = (e) => {

    e.preventDefault();

    // sementara langsung masuk dashboard
    navigate("/dashboard");
  };

  return (

    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        background: "#f5f7fa",
      }}
    >

      <div
        style={{
          width: "380px",
          background: "#fff",
          padding: "30px",
          borderRadius: "12px",
          boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
        }}
      >

        <h1
          style={{
            textAlign: "center",
            color: "#2563eb",
          }}
        >
          Mai Nexus AI
        </h1>

        <p
          style={{
            textAlign: "center",
            color: "#666",
            marginBottom: "25px",
          }}
        >
          AI Business Operating System
        </p>

        <form onSubmit={handleLogin}>

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
            style={{
              width:"100%",
              padding:"12px",
              marginBottom:"15px",
              borderRadius:"8px",
              border:"1px solid #ccc",
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
            style={{
              width:"100%",
              padding:"12px",
              marginBottom:"20px",
              borderRadius:"8px",
              border:"1px solid #ccc",
            }}
          />

          <button
            type="submit"
            style={{
              width:"100%",
              padding:"12px",
              background:"#2563eb",
              color:"#fff",
              border:"none",
              borderRadius:"8px",
              cursor:"pointer",
              fontWeight:"bold",
            }}
          >
            LOGIN
          </button>

        </form>

      </div>

    </div>

  );

}
