import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import { AvailabilitiesAPI } from "./availabilities";
import { ShiftsAPI } from "./shifts";
import { OverridesAPI } from "./overrides";
import { UsersAPI } from "./users";
import { RegistrationAPI } from "./registration";

/**
 * Configuration options for the ShiftyClient.
 */
export interface ShiftyClientOptions {
  baseURL: string;
  /**
   * Optionally provide an initial JWT token.
   */
  accessToken?: string;
}

/**
 * Main client for interacting with the Shifty API.
 */
export class ShiftyClient {
  private axios: AxiosInstance;
  private accessToken?: string;

  // Resource modules
  public availabilities: AvailabilitiesAPI;
  public shifts: ShiftsAPI;
  public overrides: OverridesAPI;
  public users: UsersAPI;
  public registration: RegistrationAPI;

  constructor(options: ShiftyClientOptions) {
    this.accessToken = options.accessToken;
    this.axios = axios.create({
      baseURL: options.baseURL,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Attach JWT token to every request if present
    this.axios.interceptors.request.use((config) => {
      if (this.accessToken) {
        config.headers = config.headers || {};
        config.headers["Authorization"] = `Bearer ${this.accessToken}`;
      }
      return config;
    });

    // Initialize resource modules
    this.availabilities = new AvailabilitiesAPI(this.axios);
    this.shifts = new ShiftsAPI(this.axios);
    this.overrides = new OverridesAPI(this.axios);
    this.users = new UsersAPI(this.axios);
    this.registration = new RegistrationAPI(this.axios);
  }

  /**
   * Set or update the JWT access token for authentication.
   */
  setAccessToken(token: string) {
    this.accessToken = token;
  }

  /**
   * Remove the JWT access token (logout).
   */
  clearAccessToken() {
    this.accessToken = undefined;
  }

  /**
   * Generic GET request.
   */
  async get<T = any>(
    url: string,
    config?: AxiosRequestConfig,
  ): Promise<AxiosResponse<T>> {
    return this.axios.get<T>(url, config);
  }

  /**
   * Generic POST request.
   */
  async post<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig,
  ): Promise<AxiosResponse<T>> {
    return this.axios.post<T>(url, data, config);
  }

  /**
   * Generic PUT request.
   */
  async put<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig,
  ): Promise<AxiosResponse<T>> {
    return this.axios.put<T>(url, data, config);
  }

  /**
   * Generic DELETE request.
   */
  async delete<T = any>(
    url: string,
    config?: AxiosRequestConfig,
  ): Promise<AxiosResponse<T>> {
    return this.axios.delete<T>(url, config);
  }

  // ==========================
  // Auth API
  // ==========================

  /**
   * Sign up a new user.
   * @returns TokenResponse
   */
  async signup(
    username: string,
    password: string,
  ): Promise<{ access_token: string }> {
    const res = await this.post<{ access_token: string }>("/auth/signup", {
      username,
      password,
    });
    return res.data;
  }

  /**
   * Log in a user.
   * @returns TokenResponse
   */
  async login(
    username: string,
    password: string,
  ): Promise<{ access_token: string }> {
    const res = await this.post<{ access_token: string }>("/auth/login", {
      username,
      password,
    });
    return res.data;
  }

  // ==========================
  // Add more resource modules below
  // ==========================
}

export default ShiftyClient;
