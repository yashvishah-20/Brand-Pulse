module.exports = {
  content: ["./pages/*.{html,js}", "./index.html", "./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#FFF4F0", // orange-50
          100: "#FFE4D6", // orange-100
          200: "#FFCAB0", // orange-200
          300: "#FFB08A", // orange-300
          400: "#FF8B5F", // orange-400
          500: "#FF6B35", // orange-500 - Lam Research orange
          600: "#E55A2B", // orange-600
          700: "#CC4A21", // orange-700
          800: "#B33A17", // orange-800
          900: "#992A0D", // orange-900
          DEFAULT: "#FF6B35", // orange-500
        },
        secondary: {
          50: "#F8F9FA", // slate-50
          100: "#F1F3F4", // slate-100
          200: "#E8EAED", // slate-200
          300: "#DADCE0", // slate-300
          400: "#BDC1C6", // slate-400
          500: "#9AA0A6", // slate-500
          600: "#80868B", // slate-600
          700: "#5F6368", // slate-700
          800: "#2C3E50", // slate-800 - Deep blue-gray
          900: "#1A252F", // slate-900
          DEFAULT: "#2C3E50", // slate-800
        },
        accent: {
          50: "#EBF8FF", // blue-50
          100: "#BEE3F8", // blue-100
          200: "#90CDF4", // blue-200
          300: "#63B3ED", // blue-300
          400: "#4299E1", // blue-400
          500: "#3498DB", // blue-500 - Clear blue
          600: "#2B77CB", // blue-600
          700: "#2C5AA0", // blue-700
          800: "#2A4365", // blue-800
          900: "#1A365D", // blue-900
          DEFAULT: "#3498DB", // blue-500
        },
        background: "#FAFBFC", // gray-50 - Warm white
        surface: "#FFFFFF", // white - Pure white
        text: {
          primary: "#2C3E50", // slate-800 - High contrast dark
          secondary: "#7F8C8D", // gray-500 - Medium gray
        },
        success: {
          50: "#F0FDF4", // green-50
          100: "#DCFCE7", // green-100
          200: "#BBF7D0", // green-200
          300: "#86EFAC", // green-300
          400: "#4ADE80", // green-400
          500: "#22C55E", // green-500
          600: "#27AE60", // green-600 - Positive sentiment
          700: "#15803D", // green-700
          800: "#166534", // green-800
          900: "#14532D", // green-900
          DEFAULT: "#27AE60", // green-600
        },
        warning: {
          50: "#FFFBEB", // amber-50
          100: "#FEF3C7", // amber-100
          200: "#FDE68A", // amber-200
          300: "#FCD34D", // amber-300
          400: "#FBBF24", // amber-400
          500: "#F39C12", // amber-500 - Neutral sentiment
          600: "#D97706", // amber-600
          700: "#B45309", // amber-700
          800: "#92400E", // amber-800
          900: "#78350F", // amber-900
          DEFAULT: "#F39C12", // amber-500
        },
        error: {
          50: "#FEF2F2", // red-50
          100: "#FEE2E2", // red-100
          200: "#FECACA", // red-200
          300: "#FCA5A5", // red-300
          400: "#F87171", // red-400
          500: "#E74C3C", // red-500 - Negative sentiment
          600: "#DC2626", // red-600
          700: "#B91C1C", // red-700
          800: "#991B1B", // red-800
          900: "#7F1D1D", // red-900
          DEFAULT: "#E74C3C", // red-500
        },
        border: {
          DEFAULT: "#E1E8ED", // gray-200
          light: "#F3F4F6", // gray-100
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        inter: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        'jetbrains': ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      fontWeight: {
        normal: '400',
        medium: '500',
        semibold: '600',
        bold: '700',
      },
      borderRadius: {
        'sm': '4px',
        'DEFAULT': '6px',
        'md': '6px',
        'lg': '8px',
        'xl': '12px',
      },
      boxShadow: {
        'card': '0 1px 3px rgba(0, 0, 0, 0.1)',
        'modal': '0 4px 12px rgba(0, 0, 0, 0.1)',
        'sm': '0 1px 3px rgba(0, 0, 0, 0.1)',
        'md': '0 4px 12px rgba(0, 0, 0, 0.1)',
      },
      transitionDuration: {
        '150': '150ms',
        '200': '200ms',
        '800': '800ms',
      },
      transitionTimingFunction: {
        'smooth': 'cubic-bezier(0.4, 0.0, 0.2, 1)',
        'out': 'ease-out',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      animation: {
        'fade-in': 'fadeIn 200ms cubic-bezier(0.4, 0.0, 0.2, 1)',
        'slide-up': 'slideUp 200ms cubic-bezier(0.4, 0.0, 0.2, 1)',
        'chart-grow': 'chartGrow 800ms cubic-bezier(0.4, 0.0, 0.2, 1)',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        chartGrow: {
          '0%': { transform: 'scaleY(0)', transformOrigin: 'bottom' },
          '100%': { transform: 'scaleY(1)', transformOrigin: 'bottom' },
        },
      },
    },
  },
  plugins: [],
}