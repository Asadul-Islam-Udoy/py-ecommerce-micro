import axios from "axios";

export const apiClient = axios.create({
  baseURL:process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  withCredentials: true,
})


apiClient.interceptors.request.use(
    (res)=>res,(error)=>{
        const message = error.response?.data?.message || "An error occurred while processing the request.";
        return Promise.reject(new Error(message));
    }
)