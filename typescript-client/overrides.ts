import { AxiosInstance } from "axios";

/**
 * Types for Override-related API.
 * You may want to expand these interfaces based on your backend DTOs.
 */
export interface OverrideCreate {
  // Define fields as per your API
  shift_id: string;
  start_time: string;
  end_time: string;
  reason?: string;
}

export interface OverrideRead {
  id: string;
  shift_id: string;
  start_time: string;
  end_time: string;
  reason?: string;
  // Add other fields as needed
}

export interface OverrideTake {
  user_id: string;
  start_time: string;
  end_time: string;
}

export interface ShiftRead {
  // Minimal fields for demonstration
  id: string;
  user_id: string;
  start_time: string;
  end_time: string;
}

/**
 * Overrides API module.
 */
export class OverridesAPI {
  private axios: AxiosInstance;
  private basePath = "/overrides";

  constructor(axios: AxiosInstance) {
    this.axios = axios;
  }

  /**
   * List all overrides.
   */
  async list(): Promise<OverrideRead[]> {
    const res = await this.axios.get<OverrideRead[]>(`${this.basePath}/`);
    return res.data;
  }

  /**
   * List open overrides.
   */
  async listOpen(): Promise<OverrideRead[]> {
    const res = await this.axios.get<OverrideRead[]>(`${this.basePath}/open`);
    return res.data;
  }

  /**
   * Get a specific override by ID.
   */
  async get(overrideId: string): Promise<OverrideRead> {
    const res = await this.axios.get<OverrideRead>(`${this.basePath}/${overrideId}`);
    return res.data;
  }

  /**
   * Create a new override.
   */
  async create(data: OverrideCreate): Promise<OverrideRead> {
    const res = await this.axios.post<OverrideRead>(`${this.basePath}/`, data);
    return res.data;
  }

  /**
   * Take an override (fulfill or claim it).
   */
  async take(overrideId: string, data: OverrideTake): Promise<ShiftRead[]> {
    const res = await this.axios.post<ShiftRead[]>(`${this.basePath}/${overrideId}/take`, data);
    return res.data;
  }
}
