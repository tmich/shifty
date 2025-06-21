import { AxiosInstance } from "axios";

/**
 * User types based on API expectations.
 * You may want to expand these interfaces as needed.
 */
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  // Add other fields as needed
}

export interface UserFull extends User {
  // Add additional fields for full user details
}

export interface UserCreate {
  email: string;
  full_name: string;
  role: string;
  password: string;
}

/**
 * Users API module.
 */
export class UsersAPI {
  private axios: AxiosInstance;

  constructor(axios: AxiosInstance) {
    this.axios = axios;
  }

  /**
   * List all users.
   */
  async list(): Promise<User[]> {
    const res = await this.axios.get<User[]>("/users/");
    return res.data;
  }

  /**
   * Get a user by ID.
   */
  async get(userId: string): Promise<UserFull> {
    const res = await this.axios.get<UserFull>(`/users/${userId}`);
    return res.data;
  }

  /**
   * Create a new user.
   */
  async create(user: UserCreate): Promise<UserFull> {
    const res = await this.axios.post<UserFull>("/users/", user);
    return res.data;
  }

  /**
   * Delete a user by ID.
   */
  async delete(userId: string): Promise<void> {
    await this.axios.delete(`/users/${userId}`);
  }

  /**
   * Get users by role.
   */
  async getByRole(role: string): Promise<UserFull[]> {
    const res = await this.axios.get<UserFull[]>(`/users/role/${role}`);
    return res.data;
  }
}
