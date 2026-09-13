import { request } from "./client";
import type { Customer, CustomerInput } from "../types/customer";

export const listCustomers = () => request<Customer[]>("/customers");
export const getCustomer = (id: number) => request<Customer>(`/customers/${id}`);
export const createCustomer = (payload: CustomerInput) =>
  request<Customer>("/customers", { method: "POST", body: JSON.stringify(payload) });
