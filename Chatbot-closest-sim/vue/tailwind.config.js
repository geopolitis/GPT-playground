/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,vue}"],
  darkMode: 'class', // Enable dark mode
  theme: {
    extend: {
      // Add any custom styles here
    },
  },
  variants: {
    extend: {
      // Add any necessary dark mode variants here
      textColor: ['dark'],
    },
  },
  plugins: [],
};
