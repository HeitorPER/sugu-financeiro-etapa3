import { useEffect, useState } from "react";
import { api, moeda } from "../api";
import { Card, PageHead, Alert } from "../components/ui";

const hoje = new Date().toISOString().slice(0, 10);
const VAZIO = { data: hoje, valor_total: "", id_fornecedor: "", id_orcamento: "", id_licitacao: "" };

export default function Compras() {
  const [compras, setCompras] = useState([]);
  const [fornecedores, setFornecedores] = useState([]);
  const [orcamentos, setOrcamentos] = useState([]);
  const [licitacoes, setLicitacoes] = useState([]);
  const [form, setForm] = useState(VAZIO);
  const [msg, setMsg] = useState(null);
  const [err, setErr] = useState(null);

  const carregar = () => {
    api.compras().then(setCompras);
    api.orcamentos().then(setOrcamentos);
  };
  useEffect(() => {
    carregar();
    api.fornecedores().then(setFornecedores);
    api.licitacoes().then(setLicitacoes);
  }, []);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const enviar = async (e) => {
    e.preventDefault();
    setMsg(null); setErr(null);
    try {
      const body = {
        data: form.data,
        valor_total: Number(form.valor_total),
        id_fornecedor: Number(form.id_fornecedor),
        id_orcamento: Number(form.id_orcamento),
        id_licitacao: form.id_licitacao ? Number(form.id_licitacao) : null,
      };
      const r = await api.efetuarCompra(body);
      setMsg(r.mensagem);
      setForm({ ...VAZIO });
      carregar();
    } catch (ex) {
      setErr(ex.message);
    }
  };

  const orcSel = orcamentos.find((o) => o.id_orcamento === Number(form.id_orcamento));

  return (
    <div>
      <PageHead
        title="Efetuar Compra"
        subtitle="Registra uma compra (COMPRA) vinculando FORNECEDOR e ORCAMENTO. As triggers validam regularidade fiscal e saldo, e atualizam o consumo do orcamento."
      />

      <Card title="Nova compra">
        <Alert type="ok" onClose={() => setMsg(null)}>{msg}</Alert>
        <Alert type="err" onClose={() => setErr(null)}>{err}</Alert>
        <form onSubmit={enviar}>
          <div className="form-grid">
            <div className="field">
              <label>Data *</label>
              <input type="date" value={form.data} onChange={set("data")} required />
            </div>
            <div className="field">
              <label>Valor total (R$) *</label>
              <input type="number" step="0.01" min="0.01" value={form.valor_total}
                     onChange={set("valor_total")} required placeholder="0,00" />
            </div>
            <div className="field">
              <label>Fornecedor *</label>
              <select value={form.id_fornecedor} onChange={set("id_fornecedor")} required>
                <option value="">Selecione...</option>
                {fornecedores.map((f) => (
                  <option key={f.id_fornecedor} value={f.id_fornecedor}>
                    {f.nome} ({f.regularidade_fiscal})
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>Orcamento *</label>
              <select value={form.id_orcamento} onChange={set("id_orcamento")} required>
                <option value="">Selecione...</option>
                {orcamentos.map((o) => (
                  <option key={o.id_orcamento} value={o.id_orcamento}>
                    {o.setor} / {o.projeto} — saldo {moeda(o.saldo)}
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>Licitacao (opcional)</label>
              <select value={form.id_licitacao} onChange={set("id_licitacao")}>
                <option value="">Compra direta (sem licitacao)</option>
                {licitacoes.map((l) => (
                  <option key={l.id_licitacao} value={l.id_licitacao}>
                    #{l.id_licitacao} {l.tipo} ({l.status})
                  </option>
                ))}
              </select>
            </div>
          </div>
          {orcSel && (
            <p className="muted" style={{ marginTop: 12, fontSize: 13 }}>
              Saldo disponivel no orcamento selecionado: <strong>{moeda(orcSel.saldo)}</strong>
            </p>
          )}
          <div className="form-actions">
            <button className="btn green" type="submit">Efetuar compra</button>
          </div>
        </form>
      </Card>

      <Card title={`Compras registradas (${compras.length})`}>
        <table>
          <thead>
            <tr>
              <th>#</th><th>Data</th><th>Fornecedor</th><th>Orcamento</th>
              <th className="num">Valor</th><th>Origem</th>
            </tr>
          </thead>
          <tbody>
            {compras.map((c) => (
              <tr key={c.id_compra}>
                <td className="muted">{c.id_compra}</td>
                <td>{c.data}</td>
                <td>{c.fornecedor}</td>
                <td className="muted">{c.orcamento_setor} / {c.orcamento_projeto}</td>
                <td className="num">{moeda(c.valor_total)}</td>
                <td>
                  {c.id_licitacao
                    ? <span className="badge blue">Licitacao #{c.id_licitacao}</span>
                    : <span className="badge gray">Compra direta</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
