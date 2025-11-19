import React from 'react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
  options: { value: string | number; label: string }[];
}

export function Select({ label, error, options, className = '', ...props }: SelectProps) {
  return (
    <div className="w-full">
      <label htmlFor={props.id} className="block text-sm font-medium text-slate-200 mb-1.5">
        {label}
        {props.required && <span className="text-pink-300 ml-1">*</span>}
      </label>
      <select
        {...props}
        className={`
          w-full px-4 py-2.5 bg-slate-700/50 border rounded-lg 
          text-slate-100
          focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50
          transition-colors
          ${error ? 'border-rose-400/60' : 'border-slate-600/50'}
          ${className}
        `}
      >
        <option value="" className="bg-slate-800 text-slate-200">Selecione...</option>
        {options.map((option) => (
          <option key={option.value} value={option.value} className="bg-slate-800 text-slate-200">
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1.5 text-sm text-rose-300">{error}</p>}
    </div>
  );
}

