/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.{html,j2,jinja2}",
    "./app/templates/**/*.html.j2",
    "./app/templates/**/*",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
