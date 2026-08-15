import React, { useState, useEffect, useRef, useId } from 'react';
import './AiDraftEmailButton.css';

export interface AiDraftEmailButtonProps {
  /** Callback triggered when the user clicks the draft email button. Can be asynchronous. */
  onDraft?: () => Promise<void> | void;
  /** Force disable the button (e.g. project data not reviewed or missing recipient). */
  disabled?: boolean;
  /** Custom message displayed in tooltip when button is disabled. */
  disabledTooltip?: string;
  /** Duration in milliseconds for Success/Error states before reverting to default (default: 2500ms). */
  autoResetDuration?: number;
  /** Custom label override for the default state (default: "Draft Customer Email"). */
  label?: string;
  /** Custom label override after a successful draft (e.g., "Regenerate Email"). */
  hasDrafted?: boolean;
  /** Optional extra CSS class names. */
  className?: string;
  /** Optional inline styles. */
  style?: React.CSSProperties;
}

export type ButtonState = 'idle' | 'loading' | 'success' | 'error';

/**
 * `AiDraftEmailButton` - A high-performance, accessible B2B SaaS action button
 * for initiating AI-powered customer email generation.
 */
export const AiDraftEmailButton: React.FC<AiDraftEmailButtonProps> = ({
  onDraft,
  disabled = false,
  disabledTooltip = 'Please ensure all project data is reviewed before drafting.',
  autoResetDuration = 2500,
  label = 'Draft Customer Email',
  hasDrafted = false,
  className = '',
  style,
}) => {
  const [buttonState, setButtonState] = useState<ButtonState>('idle');
  const tooltipId = useId();
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Clear timer on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const handleClick = async (e: React.MouseEvent<HTMLButtonElement>) => {
    if (disabled || buttonState === 'loading') return;

    if (timerRef.current) clearTimeout(timerRef.current);
    setButtonState('loading');

    try {
      if (onDraft) {
        await onDraft();
      } else {
        // Mock 1.5s delay if no handler passed
        await new Promise((resolve) => setTimeout(resolve, 1500));
      }
      setButtonState('success');
      
      timerRef.current = setTimeout(() => {
        setButtonState('idle');
      }, autoResetDuration);
    } catch (err) {
      console.error('AI Draft Email failed:', err);
      setButtonState('error');

      timerRef.current = setTimeout(() => {
        setButtonState('idle');
      }, autoResetDuration);
    }
  };

  // Label configuration based on dynamic state
  const getButtonContent = () => {
    switch (buttonState) {
      case 'loading':
        return {
          text: 'Drafting...',
          ariaLabel: 'Drafting email with AI, please wait...',
          icon: (
            <svg
              className="ai-draft-btn__icon ai-draft-btn__spinner"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M21 12a9 9 0 1 1-6.219-8.56" />
            </svg>
          ),
        };
      case 'success':
        return {
          text: 'Drafted!',
          ariaLabel: 'Email successfully drafted',
          icon: (
            <svg
              className="ai-draft-btn__icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ),
        };
      case 'error':
        return {
          text: 'Error!',
          ariaLabel: 'Failed to draft email',
          icon: (
            <svg
              className="ai-draft-btn__icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          ),
        };
      case 'idle':
      default:
        const currentText = hasDrafted ? 'Regenerate Email' : label;
        return {
          text: currentText,
          ariaLabel: currentText,
          icon: (
            <svg
              className="ai-draft-btn__icon ai-draft-btn__icon--primary"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              {/* Modern Sparkle + Paper Plane / Envelope icon hybrid */}
              <path d="M22 2L11 13" />
              <path d="M22 2L15 22L11 13L2 9L22 2Z" />
            </svg>
          ),
        };
    }
  };

  const { text, ariaLabel, icon } = getButtonContent();
  const isButtonDisabled = disabled || buttonState === 'loading';

  // State dynamic class names
  const stateClass =
    buttonState === 'loading'
      ? 'ai-draft-btn--loading'
      : buttonState === 'success'
      ? 'ai-draft-btn--success'
      : buttonState === 'error'
      ? 'ai-draft-btn--error'
      : '';

  return (
    <div className="ai-draft-btn-wrapper" tabIndex={disabled ? 0 : -1}>
      <button
        type="button"
        className={`ai-draft-btn ${stateClass} ${className}`.trim()}
        style={style}
        onClick={handleClick}
        disabled={isButtonDisabled}
        aria-label={ariaLabel}
        aria-busy={buttonState === 'loading'}
        aria-describedby={disabled ? tooltipId : undefined}
      >
        {icon}
        <span className="ai-draft-btn__label">{text}</span>
      </button>

      {disabled && (
        <div
          id={tooltipId}
          role="tooltip"
          className="ai-draft-tooltip ai-draft-tooltip--visible"
        >
          {disabledTooltip}
        </div>
      )}
    </div>
  );
};

export default AiDraftEmailButton;
