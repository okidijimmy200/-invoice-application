import { NavLink, Route, Routes } from "react-router-dom";
import { CustomersPage } from "./pages/CustomersPage";
import { InvoiceCreatePage } from "./pages/InvoiceCreatePage";
import { InvoiceDetailPage } from "./pages/InvoiceDetailPage";
import { InvoiceEditPage } from "./pages/InvoiceEditPage";
import { InvoicesPage } from "./pages/InvoicesPage";

export default function App() {
  return <><nav className="no-print"><NavLink to="/customers">Customers</NavLink><NavLink to="/invoices">Invoices</NavLink><NavLink to="/invoices/new">New invoice</NavLink></nav><main><Routes>
    <Route path="/" element={<InvoicesPage />} /><Route path="/customers" element={<CustomersPage />} /><Route path="/invoices" element={<InvoicesPage />} />
    <Route path="/invoices/new" element={<InvoiceCreatePage />} /><Route path="/invoices/:id" element={<InvoiceDetailPage />} /><Route path="/invoices/:id/edit" element={<InvoiceEditPage />} />
  </Routes></main></>;
}
