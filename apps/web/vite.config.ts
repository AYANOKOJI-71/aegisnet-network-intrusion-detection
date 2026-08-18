import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [".manus.computer"],
    proxy: {
      "/api": "http://127.0.0.1:4500",
      "/health": "http://127.0.0.1:4500",
      "/metrics": "http://127.0.0.1:4500"
    }
  }
});
