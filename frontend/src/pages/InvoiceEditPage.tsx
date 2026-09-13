import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { listCustomers } from "../api/customers";
import { getInvoice, updateInvoice } from "../api/invoices";
import { InvoiceForm } from "../components/InvoiceForm";
import type { Customer } from "../types/customer";
import type { Invoice, InvoiceInput } from "../types/invoice";

export function InvoiceEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [invoice, setInvoice] = useState<Invoice>();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [error, setError] = useState<string>();
  useEffect(() => { if (id) { void getInvoice(Number(id)).then(setInvoice).catch((err: Error) => setError(err.message)); void listCustomers().then(setCustomers).catch((err: Error) => setError(err.message)); } }, [id]);
  const submit = async (value: InvoiceInput) => { if (!invoice) return; try { const updated = await updateInvoice(invoice.id, value); navigate(`/invoices/${updated.id}`); } catch (err) { setError((err as Error).message); } };
  if (error) return <p className="error">{error}</p>;
  if (!invoice) return <p>Loading invoice…</p>;
  return <InvoiceForm customers={customers} invoice={invoice} onSubmit={submit} error={error} />;
}
