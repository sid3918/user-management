export type Gender = 'Male' | 'Female' | 'Other';
export type Status = 'Active' | 'Inactive';

export interface User {
  user_id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string | null;
  gender: Gender | null;
  date_of_birth: string | null;
  department: string | null;
  designation: string | null;
  status: Status;
  created_at: string;
  updated_at: string;
}


export interface UserPayload {
  first_name: string;
  last_name: string;
  email: string;
  phone?: string | null;
  gender?: Gender | null;
  date_of_birth?: string | null;
  department?: string | null;
  designation?: string | null;
  status: Status;
}