/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0F1720",       // near-black navy background
        panel: "#161F2B",     // card surface
        rail: "#1F2A38",      // dividers / borders
        signal: "#E8A33D",    // amber accent - "in progress" energy
        go: "#3FB68B",        // done/success
        stop: "#E0556F",      // high priority / blocked
        mist: "#8A96A3",      // muted text
      },
      fontFamily: {
        display: ["'Space Grotesk'", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};
