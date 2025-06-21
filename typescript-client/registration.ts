import { AxiosInstance } from "axios";

/**
 * Request and response types for registration endpoints.
 * You may want to expand these interfaces based on backend DTOs.
 */
export interface RegisterOrgRequest {
  organization_name: string;
  user_email: string;
  user_password: string;
  full_name: string;
}

export interface RegisterOrgResponse {
  org_code: string;
  message: string;
}

export interface JoinOrgRequest {
  org_code: string;
  user_email: string;
  user_password: string;
  full_name: string;
}

export interface TokenResponse {
  access_token: string;
}

/**
 * Registration API module.
 */
export class RegistrationAPI {
  private axios: AxiosInstance;

  constructor(axios: AxiosInstance) {
    this.axios = axios;
  }

  /**
   * Register a new organization.
   */
  async registerOrganization(data: RegisterOrgRequest): Promise<RegisterOrgResponse> {
    const response = await this.axios.post<RegisterOrgResponse>("/register/organization", data);
    return response.data;
  }

  /**
   * Join an existing organization.
   */
  async joinOrganization(data: JoinOrgRequest): Promise<TokenResponse> {
    const response = await this.axios.post<TokenResponse>("/register/join", data);
    return response.data;
  }
}
