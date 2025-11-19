import React from 'react';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
}

export function Textarea({ label, error, className = '', ...props }: TextareaProps) {
  return (
    <div className="w-full">
      <label htmlFor={props.id} className="block text-sm font-medium text-slate-200 mb-1.5">
        {label}
        {props.required && <span className="text-pink-300 ml-1">*</span>}
      </label>
      <textarea
        {...props}
        className={`
          w-full px-4 py-2.5 bg-slate-700/50 border rounded-lg 
          text-slate-100 placeholder:text-slate-400
          focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50
          transition-colors
          ${error ? 'border-rose-400/60' : 'border-slate-600/50'}
          ${className}
        `}
      />
      {error && <p className="mt-1.5 text-sm text-rose-300">{error}</p>}
    </div>
  );
}

