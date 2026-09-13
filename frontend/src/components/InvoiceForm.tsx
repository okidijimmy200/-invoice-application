import { useState, type FormEvent } from "react";
import type { Customer } from "../types/customer";
import type { Invoice, InvoiceInput } from "../types/invoice";
import { InvoiceLineItems } from "./InvoiceLineItems";

const today = new Date().toISOString().slice(0, 10);
const blank = (customerId = 0): InvoiceInput => ({
  customer_id: customerId,
  issue_date: today,
  due_date: today,
  items: [{ description: "", quantity: "1", unit_price: "0.00" }],
  notes: "",
  payment_terms: "",
});

function fromInvoice(invoice: Invoice): InvoiceInput {
  return {
    customer_id: invoice.customer_id,
    issue_date: invoice.issue_date,
    due_date: invoice.due_date,
    items: invoice.items.map(({ description, quantity, unit_price }) => ({ description, quantity, unit_price })),
    notes: invoice.notes,
    payment_terms: invoice.payment_terms,
  };
}

export function InvoiceForm({ customers, invoice, onSubmit, error }: {
  customers: Customer[];
  invoice?: Invoice;
  onSubmit: (value: InvoiceInput) => Promise<void>;
  error?: string;
}) {
  const [value, setValue] = useState<InvoiceInput>(invoice ? fromInvoice(invoice) : blank(customers[0]?.id));
  const submit = async (event: FormEvent) => { event.preventDefault(); await onSubmit(value); };
  return <form className="card form-grid" onSubmit={submit}>
    <h2>{invoice ? `Edit ${invoice.invoice_number}` : "New invoice"}</h2>
    {error && <p className="error">{error}</p>}
    <label>Customer<select required value={value.customer_id} onChange={(e) => setValue({ ...value, customer_id: Number(e.target.value) })}>
      <option value={0} disabled>Select a customer</option>
      {customers.map((customer) => <option value={customer.id} key={customer.id}>{customer.name}</option>)}
    </select></label>
    <div className="date-row"><label>Issue date<input type="date" required value={value.issue_date} onChange={(e) => setValue({ ...value, issue_date: e.target.value })} /></label>
      <label>Due date<input type="date" required value={value.due_date} onChange={(e) => setValue({ ...value, due_date: e.target.value })} /></label></div>
    <InvoiceLineItems items={value.items} onChange={(items) => setValue({ ...value, items })} />
    <label>Notes<textarea value={value.notes} onChange={(e) => setValue({ ...value, notes: e.target.value })} /></label>
    <label>Payment terms<textarea value={value.payment_terms} onChange={(e) => setValue({ ...value, payment_terms: e.target.value })} /></label>
    <button type="submit">{invoice ? "Save draft" : "Create draft"}</button>
  </form>;
}
