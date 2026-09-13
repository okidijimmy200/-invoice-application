import type { Customer } from "./customer";

export type InvoiceStatus = "Draft" | "Sent" | "Paid" | "Overdue" | "Cancelled";

export interface InvoiceItemInput {
  description: string;
  quantity: string;
  unit_price: string;
}

export interface InvoiceInput {
  customer_id: number;
  issue_date: string;
  due_date: string;
  items: InvoiceItemInput[];
  notes: string;
  payment_terms: string;
}

export interface InvoiceItem extends InvoiceItemInput {
  id: number;
  line_total: string;
}

export interface InvoiceListItem {
  id: number;
  invoice_number: string;
  customer_id: number;
  customer_name: string;
  issue_date: string;
  due_date: string;
  status: InvoiceStatus;
  total: string;
}

export interface Invoice extends InvoiceListItem {
  customer: Customer;
  items: InvoiceItem[];
  subtotal: string;
  tax: string;
  notes: string;
  payment_terms: string;
}
