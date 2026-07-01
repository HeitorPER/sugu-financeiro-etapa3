import { useEffect, useState } from "react";
import { api, moeda } from "../api";
import { Card, PageHead, EstadoPatrimonioBadge } from "../components/ui";

export default function Patrimonio() {
  const [itens, setItens] = useState([]);

  useEffect(() => {
    api.patrimonios().then(setItens);
  }, []);

  return (
    <div>
      <PageHead
        title="Patrimonio"
        subtitle="Bens adquiridos vinculados a compras, fornecedores e orcamentos."
      />

      <Card title={`Bens patrimoniais (${itens.length})`}>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Descricao</th>
              <th>Localizacao</th>
              <th>Estado</th>
              <th>Aquisicao</th>
              <th>Compra</th>
              <th>Fornecedor</th>
              <th>Orcamento</th>
              <th className="num">Valor da compra</th>
            </tr>
          </thead>
          <tbody>
            {itens.map((p) => (
              <tr key={p.id_patrimonio}>
                <td className="muted">{p.id_patrimonio}</td>
                <td>{p.descricao}</td>
                <td className="muted">{p.localizacao || "-"}</td>
                <td><EstadoPatrimonioBadge value={p.estado_conservacao} /></td>
                <td>{p.data_aquisicao}</td>
                <td className="muted">#{p.id_compra} em {p.data_compra}</td>
                <td>{p.fornecedor}</td>
                <td className="muted">{p.orcamento_setor} / {p.orcamento_projeto}</td>
                <td className="num">{moeda(p.valor_compra)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
