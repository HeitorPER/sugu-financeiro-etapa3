import { useEffect, useState } from "react";
import { api, moeda } from "../api";
import { Card, PageHead, Alert, Badge } from "../components/ui";

const hoje = new Date().toISOString().slice(0, 10);
const FORMAS = ["TRANSFERENCIA", "BOLETO", "EMPENHO", "PIX"];

export default function Pagamentos() {
  const [notas, setNotas] = useState([]);
  const [form, setForm] = useState({ id_nota: "", valor: "", forma_pagamento: "TRANSFERENCIA", data: hoje });
  const [msg, setMsg] = useState(null);
  const [err, setErr] = useState(null);

  const carregar = () => api.notas().then(setNotas);
  useEffect(() => { carregar(); }, []);

  const notaSel = notas.find((n) => n.id_nota === Number(form.id_nota));

  const enviar = async (e) => {
    e.preventDefault();
    setMsg(null); setErr(null);
    try {
      await api.registrarPagamento({
        id_nota: Number(form.id_nota),
        valor: Number(form.valor),
        forma_pagamento: form.forma_pagamento,
        data: form.data,
      });
      setMsg("Pagamento registrado com sucesso.");
      setForm({ id_nota: "", valor: "", forma_pagamento: "TRANSFERENCIA", data: hoje });
      carregar();
    } catch (ex) { setErr(ex.message); }
  };

  return (
    <div>
      <PageHead
        title="Pagamentos de Notas"
        subtitle="Registra pagamentos (PAGAMENTO) das notas fiscais (NOTA_FISCAL) via sp_registrar_pagamento. A trigger impede pagar acima do saldo em aberto."
      />

      <Card title="Registrar pagamento">
        <Alert type="ok" onClose={() => setMsg(null)}>{msg}</Alert>
        <Alert type="err" onClose={() => setErr(null)}>{err}</Alert>
        <form onSubmit={enviar}>
          <div className="form-grid">
            <div className="field">
              <label>Nota fiscal *</label>
              <select value={form.id_nota} onChange={(e) => setForm({ ...form, id_nota: e.target.value })} required>
                <option value="">Selecione...</option>
                {notas.map((n) => (
                  <option key={n.id_nota} value={n.id_nota}>
                    {n.numero} — saldo {moeda(n.saldo)}
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>Valor (R$) *</label>
              <input type="number" step="0.01" min="0.01" value={form.valor}
                     onChange={(e) => setForm({ ...form, valor: e.target.value })} required />
            </div>
            <div className="field">
              <label>Forma de pagamento</label>
              <select value={form.forma_pagamento}
                      onChange={(e) => setForm({ ...form, forma_pagamento: e.target.value })}>
                {FORMAS.map((f) => <option key={f}>{f}</option>)}
              </select>
            </div>
            <div className="field">
              <label>Data *</label>
              <input type="date" value={form.data}
                     onChange={(e) => setForm({ ...form, data: e.target.value })} required />
            </div>
          </div>
          {notaSel && (
            <p className="muted" style={{ marginTop: 12, fontSize: 13 }}>
              Nota {notaSel.numero}: valor {moeda(notaSel.valor)}, pago {moeda(notaSel.total_pago)},
              saldo em aberto <strong>{moeda(notaSel.saldo)}</strong>.
            </p>
          )}
          <div className="form-actions">
            <button className="btn green" type="submit">Registrar pagamento</button>
          </div>
        </form>
      </Card>

      <Card title={`Notas fiscais (${notas.length})`}>
        <table>
          <thead>
            <tr>
              <th>Numero</th><th>Fornecedor</th><th>Emissao</th>
              <th className="num">Valor</th><th className="num">Pago</th>
              <th className="num">Saldo</th><th>Situacao</th>
            </tr>
          </thead>
          <tbody>
            {notas.map((n) => (
              <tr key={n.id_nota}>
                <td>{n.numero}</td>
                <td className="muted">{n.fornecedor}</td>
                <td className="muted">{n.data_emissao}</td>
                <td className="num">{moeda(n.valor)}</td>
                <td className="num">{moeda(n.total_pago)}</td>
                <td className="num">{moeda(n.saldo)}</td>
                <td>
                  {Number(n.saldo) <= 0
                    ? <Badge kind="green">Quitada</Badge>
                    : <Badge kind="amber">Em aberto</Badge>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
