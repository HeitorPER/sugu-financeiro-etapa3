import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Proxy /api -> backend FastAPI local. Usamos 8001 para evitar conflito
// com uma instancia antiga em 8000 nesta maquina.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
});
