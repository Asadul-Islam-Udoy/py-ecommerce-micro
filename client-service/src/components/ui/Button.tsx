"use client";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  fullWidth?: boolean;
}

export const Button = ({ fullWidth, className, ...props }: ButtonProps) => {
  return (
    <button
      className={`
        py-3 font-semibold text-white rounded-xl bg-gradient-to-r from-blue-500 to-purple-600
        hover:scale-[1.02] transition
        ${fullWidth ? "w-full" : ""}
        ${className || ""}
      `}
      {...props}
    />
  );
};