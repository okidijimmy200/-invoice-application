import { useEffect, useState } from "react";
import { listCustomers } from "../api/customers";
import { createInvoice } from "../api/invoices";
import { EmptyState } from "../components/EmptyState";
import { InvoiceForm } from "../components/InvoiceForm";
import type { Customer } from "../types/customer";
import type { InvoiceInput } from "../types/invoice";
import { useNavigate } from "react-router-dom";

export function InvoiceCreatePage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [error, setError] = useState<string>();
  const navigate = useNavigate();
  useEffect(() => { void listCustomers().then(setCustomers).catch((err: Error) => setError(err.message)); }, []);
  const submit = async (value: InvoiceInput) => { try { setError(undefined); const invoice = await createInvoice(value); navigate(`/invoices/${invoice.id}`); } catch (err) { setError((err as Error).message); } };
  if (!error && customers.length === 0) return <EmptyState>Create a customer before creating an invoice.</EmptyState>;
  return <InvoiceForm customers={customers} onSubmit={submit} error={error} />;
}
