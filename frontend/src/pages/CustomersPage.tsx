import { useEffect, useState } from "react";
import { createCustomer, listCustomers } from "../api/customers";
import { CustomerForm } from "../components/CustomerForm";
import { EmptyState } from "../components/EmptyState";
import type { Customer, CustomerInput } from "../types/customer";

export function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [error, setError] = useState<string>();
  const load = () => listCustomers().then(setCustomers).catch((err: Error) => setError(err.message));
  useEffect(() => { void load(); }, []);
  const submit = async (value: CustomerInput) => { try { setError(undefined); await createCustomer(value); await load(); } catch (err) { setError((err as Error).message); } };
  return <section><CustomerForm onSubmit={submit} error={error} /><h1>Customers</h1>
    {customers.length === 0 ? <EmptyState>No customers yet.</EmptyState> : <div className="grid">{customers.map((customer) => <article className="card" key={customer.id}><h2>{customer.name}</h2><p>{customer.email}<br />{customer.phone}<br />{customer.address}</p></article>)}</div>}
  </section>;
}
