import { useState } from "react";
import Dashboard from "./pages/Dashboard.jsx";
import Fornecedores from "./pages/Fornecedores.jsx";
import Compras from "./pages/Compras.jsx";
import Licitacoes from "./pages/Licitacoes.jsx";
import Pagamentos from "./pages/Pagamentos.jsx";
import Relatorios from "./pages/Relatorios.jsx";

const MENU = [
  { id: "dashboard", label: "Painel", ico: "📊", comp: Dashboard },
  { id: "fornecedores", label: "Fornecedores", ico: "🏢", comp: Fornecedores },
  { id: "compras", label: "Efetuar Compra", ico: "🛒", comp: Compras },
  { id: "licitacoes", label: "Licitacoes", ico: "📑", comp: Licitacoes },
  { id: "pagamentos", label: "Pagamentos", ico: "💳", comp: Pagamentos },
  { id: "relatorios", label: "Relatorios", ico: "📈", comp: Relatorios },
];

export default function App() {
  const [aba, setAba] = useState("dashboard");
  const Atual = MENU.find((m) => m.id === aba).comp;

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <h1>SUGU</h1>
          <span>Financeiro e Compras</span>
        </div>
        {MENU.map((m) => (
          <button
            key={m.id}
            className={`nav-item ${aba === m.id ? "active" : ""}`}
            onClick={() => setAba(m.id)}
          >
            <span className="ico">{m.ico}</span>
            {m.label}
          </button>
        ))}
        <div className="foot">
          Etapa 3 · Acesso via aplicacao<br />Grupo Financeiro e Compras
        </div>
      </aside>
      <main className="main">
        <Atual />
      </main>
    </div>
  );
}
