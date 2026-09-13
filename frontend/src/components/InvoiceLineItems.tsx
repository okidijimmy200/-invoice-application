import type { InvoiceItemInput } from "../types/invoice";

export function InvoiceLineItems({ items, onChange }: { items: InvoiceItemInput[]; onChange: (items: InvoiceItemInput[]) => void }) {
  const update = (index: number, key: keyof InvoiceItemInput, value: string) =>
    onChange(items.map((item, itemIndex) => itemIndex === index ? { ...item, [key]: value } : item));
  return <fieldset><legend>Line items</legend>{items.map((item, index) => <div className="line-item" key={index}>
    <input aria-label={`Description ${index + 1}`} placeholder="Description" required value={item.description} onChange={(e) => update(index, "description", e.target.value)} />
    <input aria-label={`Quantity ${index + 1}`} placeholder="Qty" required inputMode="decimal" value={item.quantity} onChange={(e) => update(index, "quantity", e.target.value)} />
    <input aria-label={`Unit price ${index + 1}`} placeholder="Unit price" required inputMode="decimal" value={item.unit_price} onChange={(e) => update(index, "unit_price", e.target.value)} />
    {items.length > 1 && <button type="button" className="secondary" onClick={() => onChange(items.filter((_, itemIndex) => itemIndex !== index))}>Remove</button>}
  </div>)}<button type="button" className="secondary" onClick={() => onChange([...items, { description: "", quantity: "1", unit_price: "0.00" }])}>Add item</button></fieldset>;
}
