import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Proxy /api -> backend FastAPI (porta 8000), evitando problemas de CORS.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
});
