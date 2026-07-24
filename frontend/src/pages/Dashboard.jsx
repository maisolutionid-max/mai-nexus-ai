import StatCard from "../components/StatCard";

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      <StatCard title="Customers" value="0" />

      <StatCard title="Orders" value="0" />

      <StatCard title="AI Agents" value="4" />
    </div>
  );
}
