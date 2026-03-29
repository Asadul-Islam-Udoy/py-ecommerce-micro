"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  registerSchema,
  RegisterFormValues,
} from "@/features/auth/auth.schema";
import { AuthService } from "@/features/auth/auth.service";
import { Input } from "@/components/ui/Input";
import { useRouter } from "next/navigation";
import { useState } from "react";
import toast from "react-hot-toast";
import axios from "axios";

export default function RegisterForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormValues) => {
    try {
      setLoading(true);

      await AuthService.register({
        name: data.name,
        email: data.email,
        password: data.password,
      });

      toast.success("Account created successfully 🎉");

      setTimeout(() => {
        router.push("/login");
      }, 1000);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        const message = err.response?.data?.message || "Registration failed";
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
        Register for an Account
      </h2>

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="
          space-y-4
        "
      >
        <Input
          placeholder="Full Name"
          {...register("name")}
          error={errors.name?.message}
        />
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
        <Input
          type="password"
          placeholder="Confirm Password"
          {...register("confirmPassword")}
          error={errors.confirmPassword?.message}
        />

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
          {loading ? "Creating..." : "Create Account"}
        </button>
      </form>
      <p
        className="
          mt-6
          text-center text-white/80
        "
      >
        Already have an account?{" "}
        <a
          href="/pages/auth/login"
          className="
            underline hover:text-white
          "
        >
          Login
        </a>
      </p>
    </div>
  );
}
