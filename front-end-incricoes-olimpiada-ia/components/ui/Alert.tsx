import React from 'react';

interface AlertProps {
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  onClose?: () => void;
}

export function Alert({ type, message, onClose }: AlertProps) {
  const styles = {
    success: 'bg-emerald-400/20 border-emerald-400/40 text-emerald-200',
    error: 'bg-rose-400/20 border-rose-400/40 text-rose-200',
    info: 'bg-blue-400/20 border-blue-400/40 text-blue-200',
    warning: 'bg-amber-400/20 border-amber-400/40 text-amber-200',
  };

  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
    warning: '⚠',
  };

  return (
    <div className={`border rounded-lg p-4 mb-4 ${styles[type]} flex items-center justify-between backdrop-blur-sm`}>
      <div className="flex items-center gap-2">
        <span className="font-bold text-lg">{icons[type]}</span>
        <p className="text-sm">{message}</p>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="ml-4 text-slate-400 hover:text-slate-200 transition-colors"
          aria-label="Fechar"
        >
          ✕
        </button>
      )}
    </div>
  );
}

