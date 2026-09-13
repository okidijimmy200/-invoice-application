import { request } from "./client";
import type { Invoice, InvoiceInput, InvoiceListItem, InvoiceStatus } from "../types/invoice";

export const listInvoices = () => request<InvoiceListItem[]>("/invoices");
export const getInvoice = (id: number) => request<Invoice>(`/invoices/${id}`);
export const createInvoice = (payload: InvoiceInput) =>
  request<Invoice>("/invoices", { method: "POST", body: JSON.stringify(payload) });
export const updateInvoice = (id: number, payload: InvoiceInput) =>
  request<Invoice>(`/invoices/${id}`, { method: "PUT", body: JSON.stringify(payload) });
export const changeInvoiceStatus = (id: number, status: InvoiceStatus) =>
  request<Invoice>(`/invoices/${id}/status`, { method: "POST", body: JSON.stringify({ status }) });
