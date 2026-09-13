import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { changeInvoiceStatus, getInvoice } from "../api/invoices";
import { InvoiceStatusActions } from "../components/InvoiceStatusActions";
import { InvoiceSummary } from "../components/InvoiceSummary";
import type { Invoice, InvoiceStatus } from "../types/invoice";

export function InvoiceDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [invoice, setInvoice] = useState<Invoice>();
  const [error, setError] = useState<string>();
  useEffect(() => { if (id) void getInvoice(Number(id)).then(setInvoice).catch((err: Error) => setError(err.message)); }, [id]);
  if (error) return <p className="error">{error}</p>;
  if (!invoice) return <p>Loading invoice…</p>;
  const setStatus = async (status: InvoiceStatus) => { try { setError(undefined); setInvoice(await changeInvoiceStatus(invoice.id, status)); } catch (err) { setError((err as Error).message); } };
  return <section className="invoice-detail"><div className="page-actions no-print"><Link to="/invoices">← Invoices</Link><button className="secondary" onClick={() => window.print()}>Print invoice</button>{invoice.status === "Draft" && <button onClick={() => navigate(`/invoices/${invoice.id}/edit`)}>Edit draft</button>}</div>
    <header className="invoice-header"><div><p className="eyebrow">INVOICE</p><h1>{invoice.invoice_number}</h1></div><div><strong>{invoice.status}</strong><p>Issued: {invoice.issue_date}<br />Due: {invoice.due_date}</p></div></header>
    <section className="customer-block"><h2>Bill to</h2><p>{invoice.customer.name}<br />{invoice.customer.address}<br />{invoice.customer.email}<br />{invoice.customer.phone}</p></section>
    <div className="card table-wrap"><table><thead><tr><th>Description</th><th>Quantity</th><th>Unit price</th><th>Line total</th></tr></thead><tbody>{invoice.items.map((item) => <tr key={item.id}><td>{item.description}</td><td>{item.quantity}</td><td>${item.unit_price}</td><td>${item.line_total}</td></tr>)}</tbody></table></div>
    <InvoiceSummary invoice={invoice} />
    {(invoice.notes || invoice.payment_terms) && <section className="notes"><h2>Notes & terms</h2>{invoice.notes && <p><strong>Notes:</strong> {invoice.notes}</p>}{invoice.payment_terms && <p><strong>Payment terms:</strong> {invoice.payment_terms}</p>}</section>}
    <InvoiceStatusActions status={invoice.status} onChange={setStatus} error={error} />
  </section>;
}
