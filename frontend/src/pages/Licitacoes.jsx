import { useEffect, useState } from "react";
import { api, moeda } from "../api";
import { Card, PageHead, Alert, StatusBadge, Badge } from "../components/ui";

const hoje = new Date().toISOString().slice(0, 10);

export default function Licitacoes() {
  const [licitacoes, setLicitacoes] = useState([]);
  const [fornecedores, setFornecedores] = useState([]);
  const [sel, setSel] = useState(null);
  const [propostas, setPropostas] = useState([]);
  const [form, setForm] = useState({ valor: "", data: hoje, id_fornecedor: "" });
  const [msg, setMsg] = useState(null);
  const [err, setErr] = useState(null);

  const carregarLic = () => api.licitacoes().then(setLicitacoes);
  useEffect(() => {
    carregarLic();
    api.fornecedores().then(setFornecedores);
  }, []);

  const abrir = async (lic) => {
    setSel(lic); setMsg(null); setErr(null);
    setPropostas(await api.propostas(lic.id_licitacao));
  };

  const recarregar = async () => {
    await carregarLic();
    if (sel) {
      const atual = (await api.licitacoes()).find((l) => l.id_licitacao === sel.id_licitacao);
      setSel(atual);
      setPropostas(await api.propostas(sel.id_licitacao));
    }
  };

  const enviarProposta = async (e) => {
    e.preventDefault();
    setMsg(null); setErr(null);
    try {
      await api.criarProposta({
        valor: Number(form.valor),
        data: form.data,
        id_fornecedor: Number(form.id_fornecedor),
        id_licitacao: sel.id_licitacao,
      });
      setMsg("Proposta registrada.");
      setForm({ valor: "", data: hoje, id_fornecedor: "" });
      recarregar();
    } catch (ex) { setErr(ex.message); }
  };

  const homologar = async (idProposta) => {
    setMsg(null); setErr(null);
    try {
      const r = await api.homologar(sel.id_licitacao, idProposta);
      setMsg(r.mensagem);
      recarregar();
    } catch (ex) { setErr(ex.message); }
  };

  return (
    <div>
      <PageHead
        title="Licitacoes e Propostas"
        subtitle="Gerencia propostas (PROPOSTA + FORNECEDOR) e homologa a licitacao (LICITACAO) via procedure sp_homologar_licitacao."
      />
      <div className="row-split">
        <Card title="Licitacoes">
          <table>
            <thead>
              <tr><th>#</th><th>Tipo</th><th>Status</th><th className="num">Propostas</th><th></th></tr>
            </thead>
            <tbody>
              {licitacoes.map((l) => (
                <tr key={l.id_licitacao} style={{ background: sel?.id_licitacao === l.id_licitacao ? "#eff6ff" : "" }}>
                  <td className="muted">{l.id_licitacao}</td>
                  <td>{l.tipo}</td>
                  <td><StatusBadge value={l.status} /></td>
                  <td className="num">{l.qtd_propostas}</td>
                  <td><button className="btn ghost sm" onClick={() => abrir(l)}>Abrir</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>

        <div>
          {!sel ? (
            <Card title="Detalhes"><p className="muted">Selecione uma licitacao para ver as propostas.</p></Card>
          ) : (
            <Card title={`Licitacao #${sel.id_licitacao} — ${sel.tipo}`} action={<StatusBadge value={sel.status} />}>
              <Alert type="ok" onClose={() => setMsg(null)}>{msg}</Alert>
              <Alert type="err" onClose={() => setErr(null)}>{err}</Alert>

              <table>
                <thead>
                  <tr><th>Fornecedor</th><th className="num">Valor</th><th>Situacao</th><th></th></tr>
                </thead>
                <tbody>
                  {propostas.map((p) => (
                    <tr key={p.id_proposta}>
                      <td>{p.fornecedor}</td>
                      <td className="num">{moeda(p.valor)}</td>
                      <td>{p.vencedora
                        ? <Badge kind="green">Vencedora</Badge>
                        : <Badge kind="gray">—</Badge>}</td>
                      <td>
                        {sel.status !== "HOMOLOGADA" && (
                          <button className="btn sm" onClick={() => homologar(p.id_proposta)}>
                            Homologar
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                  {propostas.length === 0 && (
                    <tr><td colSpan={4} className="muted">Sem propostas.</td></tr>
                  )}
                </tbody>
              </table>

              <h4 style={{ margin: "20px 0 10px", fontSize: 14 }}>Nova proposta</h4>
              <form onSubmit={enviarProposta}>
                <div className="form-grid">
                  <div className="field">
                    <label>Fornecedor</label>
                    <select value={form.id_fornecedor}
                            onChange={(e) => setForm({ ...form, id_fornecedor: e.target.value })} required>
                      <option value="">Selecione...</option>
                      {fornecedores.map((f) => (
                        <option key={f.id_fornecedor} value={f.id_fornecedor}>{f.nome}</option>
                      ))}
                    </select>
                  </div>
                  <div className="field">
                    <label>Valor (R$)</label>
                    <input type="number" step="0.01" min="0.01" value={form.valor}
                           onChange={(e) => setForm({ ...form, valor: e.target.value })} required />
                  </div>
                  <div className="field">
                    <label>Data</label>
                    <input type="date" value={form.data}
                           onChange={(e) => setForm({ ...form, data: e.target.value })} required />
                  </div>
                </div>
                <div className="form-actions">
                  <button className="btn" type="submit">Registrar proposta</button>
                </div>
              </form>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
