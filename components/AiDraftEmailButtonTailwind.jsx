import React, { useState, useEffect, useRef, useId } from 'react';

/**
 * `AiDraftEmailButtonTailwind`
 * Tailwind CSS Variant of the AiDraftEmailButton component for React apps using Tailwind CSS v3+.
 */
export const AiDraftEmailButtonTailwind = ({
  onDraft,
  disabled = false,
  disabledTooltip = 'Please ensure all project data is reviewed before drafting.',
  autoResetDuration = 2500,
  label = 'Draft Customer Email',
  hasDrafted = false,
  className = '',
}) => {
  const [buttonState, setButtonState] = useState('idle'); // 'idle' | 'loading' | 'success' | 'error'
  const tooltipId = useId();
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const handleClick = async (e) => {
    if (disabled || buttonState === 'loading') return;

    if (timerRef.current) clearTimeout(timerRef.current);
    setButtonState('loading');

    try {
      if (onDraft) {
        await onDraft();
      } else {
        // Default async simulation
        await new Promise((resolve) => setTimeout(resolve, 1500));
      }
      setButtonState('success');
      timerRef.current = setTimeout(() => setButtonState('idle'), autoResetDuration);
    } catch (err) {
      console.error('Draft error:', err);
      setButtonState('error');
      timerRef.current = setTimeout(() => setButtonState('idle'), autoResetDuration);
    }
  };

  // Base and state dynamic styling classes
  const getDynamicStyles = () => {
    switch (buttonState) {
      case 'loading':
        return 'bg-gradient-to-r from-indigo-700 to-indigo-600 cursor-wait shadow-md';
      case 'success':
        return 'bg-gradient-to-r from-emerald-600 to-emerald-500 shadow-lg shadow-emerald-500/30 scale-100 animate-pulse';
      case 'error':
        return 'bg-gradient-to-r from-red-600 to-red-500 shadow-lg shadow-red-500/30 animate-bounce';
      case 'idle':
      default:
        if (disabled) {
          return 'bg-gray-200 text-gray-400 cursor-not-allowed shadow-none border-none';
        }
        return 'bg-gradient-to-r from-indigo-600 to-indigo-500 text-white shadow-md hover:from-indigo-700 hover:to-indigo-600 hover:shadow-lg hover:shadow-indigo-500/30 hover:-translate-y-0.5 active:bg-indigo-700 active:translate-y-0.5 active:shadow-inner active:scale-[0.98]';
    }
  };

  return (
    <div className="relative inline-block group" tabIndex={disabled ? 0 : -1}>
      <button
        type="button"
        onClick={handleClick}
        disabled={disabled || buttonState === 'loading'}
        aria-label={
          buttonState === 'loading'
            ? 'Drafting email with AI'
            : buttonState === 'success'
            ? 'Email drafted successfully'
            : buttonState === 'error'
            ? 'Error drafting email'
            : hasDrafted ? 'Regenerate Email' : label
        }
        aria-busy={buttonState === 'loading'}
        aria-describedby={disabled ? tooltipId : undefined}
        className={`inline-flex items-center justify-center gap-2.5 px-5 py-3 rounded-lg font-sans font-semibold text-base leading-6 transition-all duration-200 ease-in-out select-none outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-indigo-500 ${getDynamicStyles()} ${className}`}
      >
        {/* Dynamic Icon */}
        {buttonState === 'loading' && (
          <svg
            className="w-5 h-5 animate-spin text-white"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
          </svg>
        )}

        {buttonState === 'success' && (
          <svg
            className="w-5 h-5 text-white"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <polyline points="20 6 9 17 4 12" />
          </svg>
        )}

        {buttonState === 'error' && (
          <svg
            className="w-5 h-5 text-white"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        )}

        {buttonState === 'idle' && (
          <svg
            className={`w-5 h-5 transition-transform duration-200 ${
              disabled
                ? 'opacity-40'
                : 'group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:scale-105'
            }`}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M22 2L11 13" />
            <path d="M22 2L15 22L11 13L2 9L22 2Z" />
          </svg>
        )}

        {/* Dynamic Label */}
        <span>
          {buttonState === 'loading'
            ? 'Drafting...'
            : buttonState === 'success'
            ? 'Drafted!'
            : buttonState === 'error'
            ? 'Error!'
            : hasDrafted
            ? 'Regenerate Email'
            : label}
        </span>
      </button>

      {/* Accessible Tooltip for Disabled State */}
      {disabled && (
        <div
          id={tooltipId}
          role="tooltip"
          className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w.max max-w-xs px-3 py-1.5 bg-gray-900 text-white text-xs font-medium rounded shadow-xl opacity-0 pointer-events-none transition-all duration-200 group-hover:opacity-100 group-hover:-translate-y-1 group-focus-within:opacity-100 group-focus-within:-translate-y-1 z-50 text-center"
        >
          {disabledTooltip}
          <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900" />
        </div>
      )}
    </div>
  );
};

export default AiDraftEmailButtonTailwind;
