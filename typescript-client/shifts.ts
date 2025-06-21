import { AxiosInstance } from "axios";

/**
 * Shift entity (partial, extend as needed)
 */
export interface Shift {
  id: string;
  user_id: string;
  start: string; // ISO datetime
  end: string;   // ISO datetime
  // ...other fields
}

export interface ShiftCreate {
  user_id: string;
  start: string;
  end: string;
  // ...other fields
}

export interface ShiftUpdate {
  start?: string;
  end?: string;
  // ...other updatable fields
}

export class ShiftsAPI {
  private axios: AxiosInstance;
  private basePath = "/shifts";

  constructor(axios: AxiosInstance) {
    this.axios = axios;
  }

  /**
   * List all shifts.
   */
  async list(): Promise<Shift[]> {
    const res = await this.axios.get<Shift[]>(`${this.basePath}/`);
    return res.data;
  }

  /**
   * Get a shift by ID.
   */
  async get(shiftId: string): Promise<Shift> {
    const res = await this.axios.get<Shift>(`${this.basePath}/${shiftId}`);
    return res.data;
  }

  /**
   * Create a new shift.
   */
  async create(data: ShiftCreate): Promise<Shift> {
    const res = await this.axios.post<Shift>(`${this.basePath}/`, data);
    return res.data;
  }

  /**
   * Update a shift by ID.
   */
  async update(shiftId: string, data: ShiftUpdate): Promise<Shift> {
    const res = await this.axios.put<Shift>(`${this.basePath}/${shiftId}`, data);
    return res.data;
  }

  /**
   * Delete a shift by ID.
   */
  async delete(shiftId: string): Promise<void> {
    await this.axios.delete(`${this.basePath}/${shiftId}`);
  }
}
