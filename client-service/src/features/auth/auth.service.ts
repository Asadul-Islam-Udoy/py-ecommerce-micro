import { apiClient } from "@/lib/axios";

export interface RegisterDTO {
  name: string;
  email: string;
  password: string;
}

export const AuthService = {
  register: async (data: RegisterDTO) => {
    const res = await apiClient.post("/users/register/", data);
    return res.data;
  },

  login: async (data: { email: string; password: string }) => {
    const res = await apiClient.post("/users/login/", data);
    return res.data;
  },
};