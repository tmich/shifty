import { AxiosInstance } from "axios";

// --- DTOs (simplified, adjust as needed) ---
export interface AvailabilityCreate {
  user_id: string;
  date: string; // YYYY-MM-DD
  start_time: string; // HH:MM
  end_time: string;   // HH:MM
}

export interface AvailabilityUpdate {
  start_time?: string;
  end_time?: string;
}

export interface AvailabilityFull {
  id: string;
  user_id: string;
  date: string;
  start_time: string;
  end_time: string;
  // Add other fields as needed
}

export interface AvailabilityResult {
  result: string;
  message: string;
  availability?: AvailabilityFull;
}

// --- Availabilities API Module ---
export class AvailabilitiesAPI {
  private axios: AxiosInstance;
  private basePath = "/availabilities";

  constructor(axios: AxiosInstance) {
    this.axios = axios;
  }

  // List all availabilities
  async list(): Promise<AvailabilityFull[]> {
    const res = await this.axios.get<AvailabilityFull[]>(`${this.basePath}/`);
    return res.data;
  }

  // Get a single availability by ID
  async get(availabilityId: string): Promise<AvailabilityFull | null> {
    const res = await this.axios.get<AvailabilityFull | null>(`${this.basePath}/${availabilityId}`);
    return res.data;
  }

  // Create a new availability
  async create(data: AvailabilityCreate): Promise<AvailabilityResult> {
    const res = await this.axios.post<AvailabilityResult>(`${this.basePath}/`, data);
    return res.data;
  }

  // Update an availability
  async update(availabilityId: string, data: AvailabilityUpdate): Promise<AvailabilityFull> {
    const res = await this.axios.put<AvailabilityFull>(`${this.basePath}/${availabilityId}`, data);
    return res.data;
  }

  // Delete an availability
  async delete(availabilityId: string): Promise<void> {
    await this.axios.delete(`${this.basePath}/${availabilityId}`);
  }

  // Get availabilities by user
  async getByUser(userId: string): Promise<AvailabilityFull[]> {
    const res = await this.axios.get<AvailabilityFull[]>(`${this.basePath}/user/${userId}`);
    return res.data;
  }

  // Get availabilities by user and date
  async getByUserAndDate(userId: string, date: string): Promise<AvailabilityFull[]> {
    const res = await this.axios.get<AvailabilityFull[]>(`${this.basePath}/user/${userId}/date/${date}`);
    return res.data;
  }

  // Get availabilities by date
  async getByDate(date: string): Promise<AvailabilityFull[]> {
    const res = await this.axios.get<AvailabilityFull[]>(`${this.basePath}/date/${date}`);
    return res.data;
  }
}
