import { useEffect, useState } from "react";
import { api } from "../api";
import { Card, PageHead, Alert, RegularidadeBadge } from "../components/ui";

const VAZIO = { nome: "", cnpj: "", endereco: "", telefone: "", regularidade_fiscal: "PENDENTE" };

export default function Fornecedores() {
  const [lista, setLista] = useState([]);
  const [form, setForm] = useState(VAZIO);
  const [msg, setMsg] = useState(null);
  const [err, setErr] = useState(null);

  const carregar = () => api.fornecedores().then(setLista);
  useEffect(() => { carregar(); }, []);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const enviar = async (e) => {
    e.preventDefault();
    setMsg(null); setErr(null);
    try {
      const r = await api.criarFornecedor(form);
      setMsg(r.mensagem);
      setForm(VAZIO);
      carregar();
    } catch (ex) {
      setErr(ex.message);
    }
  };

  const mudarReg = async (id, valor) => {
    setMsg(null); setErr(null);
    try {
      await api.atualizarRegularidade(id, valor);
      setMsg("Regularidade fiscal atualizada.");
      carregar();
    } catch (ex) {
      setErr(ex.message);
    }
  };

  return (
    <div>
      <PageHead
        title="Fornecedores"
        subtitle="Cadastro de fornecedores e controle de regularidade fiscal (tabela FORNECEDOR)"
      />

      <Card title="Cadastrar novo fornecedor">
        <Alert type="ok" onClose={() => setMsg(null)}>{msg}</Alert>
        <Alert type="err" onClose={() => setErr(null)}>{err}</Alert>
        <form onSubmit={enviar}>
          <div className="form-grid">
            <div className="field">
              <label>Nome *</label>
              <input value={form.nome} onChange={set("nome")} required maxLength={100} />
            </div>
            <div className="field">
              <label>CNPJ * (min. 14 caracteres)</label>
              <input value={form.cnpj} onChange={set("cnpj")} required placeholder="00.000.000/0001-00" />
            </div>
            <div className="field">
              <label>Endereco</label>
              <input value={form.endereco} onChange={set("endereco")} />
            </div>
            <div className="field">
              <label>Telefone</label>
              <input value={form.telefone} onChange={set("telefone")} />
            </div>
            <div className="field">
              <label>Regularidade fiscal</label>
              <select value={form.regularidade_fiscal} onChange={set("regularidade_fiscal")}>
                <option>PENDENTE</option>
                <option>REGULAR</option>
                <option>IRREGULAR</option>
              </select>
            </div>
          </div>
          <div className="form-actions">
            <button className="btn" type="submit">Cadastrar fornecedor</button>
          </div>
        </form>
      </Card>

      <Card title={`Fornecedores cadastrados (${lista.length})`}>
        <table>
          <thead>
            <tr>
              <th>#</th><th>Nome</th><th>CNPJ</th><th>Telefone</th>
              <th>Regularidade</th><th>Acao</th>
            </tr>
          </thead>
          <tbody>
            {lista.map((f) => (
              <tr key={f.id_fornecedor}>
                <td className="muted">{f.id_fornecedor}</td>
                <td>{f.nome}</td>
                <td className="muted">{f.cnpj}</td>
                <td className="muted">{f.telefone}</td>
                <td><RegularidadeBadge value={f.regularidade_fiscal} /></td>
                <td>
                  <select
                    defaultValue=""
                    onChange={(e) => e.target.value && mudarReg(f.id_fornecedor, e.target.value)}
                    style={{ padding: "5px 8px", fontSize: 12.5 }}
                  >
                    <option value="" disabled>alterar...</option>
                    <option value="REGULAR">REGULAR</option>
                    <option value="PENDENTE">PENDENTE</option>
                    <option value="IRREGULAR">IRREGULAR</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
