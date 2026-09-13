import type { Invoice } from "../types/invoice";

export function InvoiceSummary({ invoice }: { invoice: Pick<Invoice, "subtotal" | "tax" | "total"> }) {
  return <dl className="totals"><div><dt>Subtotal</dt><dd>${invoice.subtotal}</dd></div><div><dt>Tax (15%)</dt><dd>${invoice.tax}</dd></div><div><dt>Total</dt><dd>${invoice.total}</dd></div></dl>;
}
