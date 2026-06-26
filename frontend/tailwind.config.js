export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        panel: "rgb(var(--color-panel) / <alpha-value>)",
        surface: "rgb(var(--color-surface) / <alpha-value>)",
        ink: "rgb(var(--color-ink) / <alpha-value>)",
        muted: "rgb(var(--color-muted) / <alpha-value>)",
        line: "rgb(var(--color-line) / <alpha-value>)",
        signal: "rgb(var(--color-signal) / <alpha-value>)",
        warning: "rgb(var(--color-warning) / <alpha-value>)",
      }
    }
  },
  plugins: [],
}
