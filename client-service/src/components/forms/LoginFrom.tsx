"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, LoginFormValues } from "@/features/auth/auth.schema";
import { AuthService } from "@/features/auth/auth.service";
import { Input } from "@/components/ui/Input";
import { useRouter } from "next/navigation";
import { useState } from "react";
import toast from "react-hot-toast";
import axios from "axios";

export default function LoginForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormValues) => {
    try {
      setLoading(true);

      await AuthService.login({
        email: data.email,
        password: data.password,
      });

      toast.success("Login successful 🎉");

      setTimeout(() => {
        router.push("/dashboard");
      }, 1000);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        const message = err.response?.data?.message || "Login failed";
        toast.error(message);
      } else if (err instanceof Error) {
        toast.error(err.message);
      } else {
        toast.error("Unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="
        w-full max-w-md
        p-8
        bg-white/10
        rounded-2xl border border-white/20
        backdrop-blur-xl shadow-2xl
      "
    >
      <h2
        className="
          mb-6
          text-3xl text-white text-center font-bold
        "
      >
        Login to Your Account
      </h2>

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="
          space-y-4
        "
      >
        <Input
          placeholder="Email"
          {...register("email")}
          error={errors.email?.message}
        />
        <Input
          type="password"
          placeholder="Password"
          {...register("password")}
          error={errors.password?.message}
        />
        <div
          className="
            flex justify-between items-center
          "
        >
          <a
            href="/forgot-password"
            className="
              text-sm text-white/80 hover:text-white underline
            "
          >
            Forgot Password?
          </a>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="
            w-full
            py-3
            text-white font-semibold
            bg-gradient-to-r from-blue-500 to-purple-600
            rounded-xl
            transition
            hover:scale-[1.02]
            cursor-pointer
          "
        >
          {loading ? "Login..." : "Login"}
        </button>
      </form>
      <p
        className="
          mt-6
          text-center text-white/80
        "
      >
        Don&apos;t have an account?{" "}
        <a
          href="/pages/auth/registration"
          className="
            underline hover:text-white font-semibold
          "
        >
          Register
        </a>
      </p>
    </div>
  );
}
