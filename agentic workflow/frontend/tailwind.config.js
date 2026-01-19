/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Inside Out theme colors
        'insideout': {
          'joy': '#FFD700',
          'joy-glow': '#FFF8DC',
          'sadness': '#5B8DD9',
          'sadness-deep': '#2E4A7D',
          'anger': '#E53935',
          'fear': '#9C27B0',
          'disgust': '#4CAF50',
          'anxiety': '#FF6F00',
        },
        // Memory orb colors
        'memory': {
          'gold': '#FFD54F',
          'blue': '#64B5F6',
          'red': '#EF5350',
          'purple': '#BA68C8',
          'green': '#81C784',
          'pink': '#F48FB1',
          'cyan': '#4DD0E1',
        },
        // UI colors
        'hq': {
          'dark': '#1a1a2e',
          'purple': '#4a1a6b',
          'magenta': '#6b2d5c',
          'blue': '#16213e',
          'glow': '#a855f7',
        }
      },
      fontFamily: {
        'display': ['Fredoka One', 'Comic Sans MS', 'cursive'],
        'body': ['Nunito', 'sans-serif'],
      },
      animation: {
        'glow-pulse': 'glow-pulse 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'float-slow': 'float 5s ease-in-out infinite',
        'float-delayed': 'float 4s ease-in-out infinite 1s',
        'orb-enter': 'orb-enter 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards',
        'sparkle': 'sparkle 1.5s ease-in-out infinite',
        'bounce-gentle': 'bounce-gentle 2s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'memory-stream': 'memory-stream 20s linear infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
      },
      keyframes: {
        'glow-pulse': {
          '0%, 100%': { boxShadow: '0 0 20px 5px rgba(168, 85, 247, 0.4)' },
          '50%': { boxShadow: '0 0 40px 15px rgba(168, 85, 247, 0.6)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0) rotate(0deg)' },
          '50%': { transform: 'translateY(-15px) rotate(2deg)' },
        },
        'orb-enter': {
          '0%': { transform: 'scale(0) translateY(50px)', opacity: '0' },
          '60%': { transform: 'scale(1.3) translateY(-15px)', opacity: '1' },
          '100%': { transform: 'scale(1) translateY(0)', opacity: '1' },
        },
        'sparkle': {
          '0%, 100%': { opacity: '0.5', transform: 'scale(1)' },
          '50%': { opacity: '1', transform: 'scale(1.2)' },
        },
        'bounce-gentle': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        'shimmer': {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        'memory-stream': {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: '0.6' },
          '50%': { opacity: '1' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'shimmer-gradient': 'linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)',
      },
      boxShadow: {
        'joy': '0 0 30px 10px rgba(255, 215, 0, 0.5)',
        'sadness': '0 0 30px 10px rgba(91, 141, 217, 0.5)',
        'anger': '0 0 30px 10px rgba(229, 57, 53, 0.5)',
        'fear': '0 0 30px 10px rgba(156, 39, 176, 0.5)',
        'memory': '0 0 20px 5px rgba(255, 255, 255, 0.3)',
        'glow-purple': '0 0 40px 10px rgba(168, 85, 247, 0.4)',
        'glow-gold': '0 0 40px 10px rgba(255, 215, 0, 0.4)',
      }
    },
  },
  plugins: [],
}
