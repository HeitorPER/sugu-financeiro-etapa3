import { useEffect, useState } from "react";
import { api, moeda } from "../api";
import { Card, PageHead, ProgressBar, RegularidadeBadge } from "../components/ui";

export default function Relatorios() {
  const [ano, setAno] = useState(2024);
  const [relAno, setRelAno] = useState([]);
  const [top, setTop] = useState([]);

  const carregarAno = (a) => api.relOrcamentos(a).then(setRelAno);
  useEffect(() => {
    carregarAno(ano);
    api.relFornecedoresTop().then(setTop);
  }, []);

  const trocarAno = (a) => { setAno(a); carregarAno(a); };

  return (
    <div>
      <PageHead
        title="Relatorios Gerenciais"
        subtitle="Consultas analiticas combinando ORCAMENTO, COMPRA e FORNECEDOR (procedure sp_relatorio_orcamento e agregacoes)."
      />

      <Card
        title="Saldo dos orcamentos por ano"
        action={
          <select value={ano} onChange={(e) => trocarAno(Number(e.target.value))}>
            <option value={2024}>2024</option>
            <option value={2025}>2025</option>
          </select>
        }
      >
        <table>
          <thead>
            <tr>
              <th>Setor</th><th>Projeto</th>
              <th className="num">Total</th><th className="num">Consumido</th>
              <th className="num">Saldo</th><th>% consumido</th>
            </tr>
          </thead>
          <tbody>
            {relAno.map((o) => (
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

      <Card title="Ranking de fornecedores que mais venderam">
        <table>
          <thead>
            <tr>
              <th>#</th><th>Fornecedor</th><th>Regularidade</th>
              <th className="num">Compras</th><th className="num">Total vendido</th>
            </tr>
          </thead>
          <tbody>
            {top.map((f, i) => (
              <tr key={f.id_fornecedor}>
                <td className="muted">{i + 1}</td>
                <td>{f.nome}</td>
                <td><RegularidadeBadge value={f.regularidade_fiscal} /></td>
                <td className="num">{f.qtd_compras}</td>
                <td className="num">{moeda(f.total_vendido)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
