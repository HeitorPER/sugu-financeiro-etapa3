// Pequenos componentes reutilizaveis de UI.

export function Badge({ kind, children }) {
  return <span className={`badge ${kind}`}>{children}</span>;
}

const REG_KIND = { REGULAR: "green", PENDENTE: "amber", IRREGULAR: "red" };
export function RegularidadeBadge({ value }) {
  return <Badge kind={REG_KIND[value] || "gray"}>{value}</Badge>;
}

const LIC_KIND = {
  ABERTA: "green", EM_ANALISE: "blue", HOMOLOGADA: "blue",
  CANCELADA: "red", DESERTA: "amber",
};
export function StatusBadge({ value }) {
  return <Badge kind={LIC_KIND[value] || "gray"}>{value}</Badge>;
}

export function Alert({ type, children, onClose }) {
  if (!children) return null;
  return (
    <div className={`alert ${type}`} onClick={onClose} role="alert">
      {children}
    </div>
  );
}

export function ProgressBar({ pct }) {
  const cls = pct >= 80 ? "danger" : pct >= 50 ? "warn" : "";
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 8 }}>
      <span className={`bar ${cls}`}>
        <span style={{ width: `${Math.min(pct, 100)}%` }} />
      </span>
      <span className="muted" style={{ fontSize: 12 }}>{pct}%</span>
    </span>
  );
}

export function Card({ title, action, children }) {
  return (
    <div className="card">
      {(title || action) && (
        <div className="card-head">
          <h3>{title}</h3>
          {action}
        </div>
      )}
      <div className="card-body">{children}</div>
    </div>
  );
}

export function PageHead({ title, subtitle }) {
  return (
    <div className="page-head">
      <h2>{title}</h2>
      <p>{subtitle}</p>
    </div>
  );
}
