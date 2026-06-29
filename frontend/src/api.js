// Cliente HTTP simples para a API FastAPI. Centraliza fetch e tratamento de erro.
const BASE = "/api";

async function request(path, options = {}) {
  const res = await fetch(BASE + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || "Erro inesperado na requisicao.");
  }
  return data;
}

export const api = {
  dashboard: () => request("/dashboard"),

  // Fornecedores
  fornecedores: () => request("/fornecedores"),
  criarFornecedor: (body) =>
    request("/fornecedores", { method: "POST", body: JSON.stringify(body) }),
  atualizarRegularidade: (id, regularidade_fiscal) =>
    request(`/fornecedores/${id}/regularidade`, {
      method: "PUT",
      body: JSON.stringify({ regularidade_fiscal }),
    }),

  // Compras / Orcamentos
  orcamentos: () => request("/orcamentos"),
  compras: () => request("/compras"),
  efetuarCompra: (body) =>
    request("/compras", { method: "POST", body: JSON.stringify(body) }),

  // Licitacoes / Propostas
  licitacoes: () => request("/licitacoes"),
  propostas: (idLic) => request(`/licitacoes/${idLic}/propostas`),
  criarProposta: (body) =>
    request("/propostas", { method: "POST", body: JSON.stringify(body) }),
  homologar: (idLic, id_proposta) =>
    request(`/licitacoes/${idLic}/homologar`, {
      method: "POST",
      body: JSON.stringify({ id_proposta }),
    }),

  // Notas / Pagamentos
  notas: () => request("/notas"),
  registrarPagamento: (body) =>
    request("/pagamentos", { method: "POST", body: JSON.stringify(body) }),

  // Relatorios
  relOrcamentos: (ano) => request(`/relatorios/orcamentos?ano=${ano}`),
  relFornecedoresTop: () => request("/relatorios/fornecedores-top"),
  relOrcamentosConsumo: () => request("/relatorios/orcamentos-consumo"),
};

export const moeda = (v) =>
  Number(v).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
