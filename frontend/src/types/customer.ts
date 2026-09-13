export interface Customer {
  id: number;
  name: string;
  phone: string;
  email: string;
  address: string;
}

export type CustomerInput = Omit<Customer, "id">;
