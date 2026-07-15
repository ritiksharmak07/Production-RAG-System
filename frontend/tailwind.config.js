/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef7ff',
          100: '#dbeeff',
          500: '#2563eb',
          700: '#1d4ed8',
        },
      },
    },
  },
  plugins: [],
}
