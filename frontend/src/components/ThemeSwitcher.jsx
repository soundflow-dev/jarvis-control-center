import { Monitor, Moon, Sun } from "lucide-react"

import { useI18n } from "../i18n"
import { useTheme } from "../theme"

const options = [
  { value: "system", icon: Monitor, labelKey: "theme.system" },
  { value: "dark", icon: Moon, labelKey: "theme.dark" },
  { value: "light", icon: Sun, labelKey: "theme.light" },
]

export function ThemeSwitcher() {
  const { t } = useI18n()
  const { theme, setTheme } = useTheme()

  return (
    <div className="inline-flex rounded-md border border-line bg-panel p-1 shadow-sm" aria-label={t("theme.label")}>
      {options.map((option) => {
        const Icon = option.icon
        const selected = theme === option.value
        return (
          <button
            key={option.value}
            className={`grid h-8 w-8 place-items-center rounded text-muted transition hover:text-ink ${selected ? "bg-surface text-signal shadow-sm" : ""}`}
            type="button"
            onClick={() => setTheme(option.value)}
            title={t(option.labelKey)}
            aria-label={t(option.labelKey)}
            aria-pressed={selected}
          >
            <Icon size={16} aria-hidden="true" />
          </button>
        )
      })}
    </div>
  )
}
