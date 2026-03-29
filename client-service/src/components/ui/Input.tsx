interface Props extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

export const Input = ({ error, ...props }: Props) => {
  return (
    <div>
      <input
        {...props}
        className="
          w-full
          p-3
          text-white
          bg-white/10
          rounded-xl border border-white/20 focus:ring-2 focus:ring-blue-500
          outline-none
        "
        /
      >
      {error && (
        <p
          className="
            mt-1
            text-red-400 text-sm
          "
        >
          {error}
        </p>
      )}
    </div>
  );
};
