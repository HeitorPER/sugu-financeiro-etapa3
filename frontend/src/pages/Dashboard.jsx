import { useEffect, useState } from "react";
import { api, moeda } from "../api";
import { Card, PageHead, ProgressBar } from "../components/ui";

export default function Dashboard() {
  const [kpi, setKpi] = useState(null);
  const [consumo, setConsumo] = useState([]);

  useEffect(() => {
    api.dashboard().then(setKpi);
    api.relOrcamentosConsumo().then(setConsumo);
  }, []);

  if (!kpi) return <div className="spin">Carregando...</div>;

  return (
    <div>
      <PageHead
        title="Painel Financeiro"
        subtitle="Visao geral do subsistema Financeiro e de Compras do SUGU"
      />
      <div className="kpi-grid" style={{ marginBottom: 24 }}>
        <div className="kpi">
          <div className="label">Fornecedores</div>
          <div className="value">{kpi.fornecedores}</div>
          <div className="muted" style={{ fontSize: 12 }}>
            {kpi.fornecedores_regulares} regulares
          </div>
        </div>
        <div className="kpi">
          <div className="label">Compras efetuadas</div>
          <div className="value">{kpi.compras}</div>
        </div>
        <div className="kpi">
          <div className="label">Total comprado</div>
          <div className="value sm">{moeda(kpi.total_comprado)}</div>
        </div>
        <div className="kpi">
          <div className="label">Licitacoes abertas</div>
          <div className="value">{kpi.licitacoes_abertas}</div>
        </div>
        <div className="kpi">
          <div className="label">Saldo orcamentario</div>
          <div className="value sm">{moeda(kpi.saldo_total)}</div>
        </div>
      </div>

      <Card title="Consumo dos orcamentos">
        <table>
          <thead>
            <tr>
              <th>Setor</th>
              <th>Projeto</th>
              <th className="num">Total</th>
              <th className="num">Consumido</th>
              <th className="num">Saldo</th>
              <th>Consumo</th>
            </tr>
          </thead>
          <tbody>
            {consumo.map((o) => (
              <tr key={o.id_orcamento}>
                <td>{o.setor}</td>
                <td className="muted">{o.projeto}</td>
                <td className="num">{moeda(o.valor_total)}</td>
                <td className="num">{moeda(o.valor_consumido)}</td>
                <td className="num">{moeda(o.saldo)}</td>
                <td><ProgressBar pct={Number(o.pct_consumido)} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
