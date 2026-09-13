import { useState, type FormEvent } from "react";
import type { CustomerInput } from "../types/customer";

const empty: CustomerInput = { name: "", phone: "", email: "", address: "" };

export function CustomerForm({ onSubmit, error }: { onSubmit: (value: CustomerInput) => Promise<void>; error?: string }) {
  const [value, setValue] = useState<CustomerInput>(empty);
  const submit = async (event: FormEvent) => {
    event.preventDefault();
    await onSubmit(value);
    setValue(empty);
  };
  return <form className="card form-grid" onSubmit={submit}>
    <h2>New customer</h2>
    {error && <p className="error">{error}</p>}
    {(["name", "phone", "email", "address"] as const).map((field) => <label key={field}>
      {field[0].toUpperCase() + field.slice(1)}
      <input type={field === "email" ? "email" : "text"} required value={value[field]}
        onChange={(event) => setValue({ ...value, [field]: event.target.value })} />
    </label>)}
    <button type="submit">Create customer</button>
  </form>;
}
