import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listInvoices } from "../api/invoices";
import { EmptyState } from "../components/EmptyState";
import type { InvoiceListItem } from "../types/invoice";

export function InvoicesPage() {
  const [invoices, setInvoices] = useState<InvoiceListItem[]>([]);
  const [error, setError] = useState<string>();
  useEffect(() => { void listInvoices().then(setInvoices).catch((err: Error) => setError(err.message)); }, []);
  if (error) return <p className="error">{error}</p>;
  if (!invoices.length) return <EmptyState>No invoices yet.</EmptyState>;
  return <section><h1>Invoices</h1><div className="card table-wrap"><table><thead><tr><th>Number</th><th>Customer</th><th>Issue</th><th>Due</th><th>Status</th><th>Total</th></tr></thead><tbody>
    {invoices.map((invoice) => <tr key={invoice.id}><td><Link to={`/invoices/${invoice.id}`}>{invoice.invoice_number}</Link></td><td>{invoice.customer_name}</td><td>{invoice.issue_date}</td><td>{invoice.due_date}</td><td>{invoice.status}</td><td>${invoice.total}</td></tr>)}
  </tbody></table></div></section>;
}
