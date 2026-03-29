import LoginForm from "@/components/forms/LoginFrom";

export default function RegisterPage() {
  return (
    <div
      className="
        flex items-center justify-center
        min-h-screen
        bg-gradient-to-br from-black via-gray-900 to-gray-800
      "
    >
      <LoginForm />
    </div>
  );
}