import type { InvoiceStatus } from "../types/invoice";

const next: Record<InvoiceStatus, InvoiceStatus[]> = {
  Draft: ["Sent", "Cancelled"], Sent: ["Paid", "Overdue", "Cancelled"], Overdue: ["Cancelled"], Paid: [], Cancelled: [],
};

export function InvoiceStatusActions({ status, onChange, error }: { status: InvoiceStatus; onChange: (status: InvoiceStatus) => Promise<void>; error?: string }) {
  return <div className="actions no-print"><h3>Status: {status}</h3>{error && <p className="error">{error}</p>}
    {next[status].map((target) => <button key={target} className="secondary" onClick={() => void onChange(target)}>Mark {target}</button>)}</div>;
}
