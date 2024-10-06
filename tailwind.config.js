/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./views/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        asap: ['Asap', 'sans-serif'],  // Define the Asap font family
        inter: ['Inter', 'Arial', 'sans-serif'],
      },
      colors: {
        'primary-color': '#001F3F',
        'secondary-color': '#f62d00',
        'accent-color': '#B2B2B2',        
      },
    },
  },
  plugins: [],
}