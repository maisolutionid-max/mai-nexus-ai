import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/mai-nexus-ai/",
  server: {
    port: 5173,
  },
});
