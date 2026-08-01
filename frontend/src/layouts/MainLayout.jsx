import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function MainLayout({ children }) {

  return (

    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        background: "#f5f7fa",
      }}
    >

      <Sidebar />

      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
        }}
      >

        <Navbar />

        <div
          style={{
            padding: "20px",
          }}
        >
          {children}
        </div>

      </div>

    </div>

  );

}
