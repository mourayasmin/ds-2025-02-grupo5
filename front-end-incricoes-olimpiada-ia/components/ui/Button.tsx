import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  isLoading?: boolean;
}

export function Button({
  children,
  variant = 'primary',
  isLoading = false,
  disabled,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles = 'px-6 py-2.5 rounded-lg font-medium transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-800';
  
  const variantStyles = {
    primary: 'bg-blue-400/80 text-slate-900 hover:bg-blue-400 focus:ring-blue-400/50 disabled:bg-blue-400/30 disabled:text-slate-500 shadow-lg shadow-blue-400/20',
    secondary: 'bg-slate-600/60 text-slate-200 hover:bg-slate-600/80 focus:ring-slate-500/50 disabled:bg-slate-700/30 disabled:text-slate-500',
    danger: 'bg-rose-400/80 text-slate-900 hover:bg-rose-400 focus:ring-rose-400/50 disabled:bg-rose-400/30 disabled:text-slate-500',
  };

  return (
    <button
      {...props}
      disabled={disabled || isLoading}
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
    >
      {isLoading ? (
        <span className="flex items-center gap-2">
          <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Processando...
        </span>
      ) : (
        children
      )}
    </button>
  );
}

