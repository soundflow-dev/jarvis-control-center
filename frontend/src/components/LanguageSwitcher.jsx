import { languages, useI18n } from "../i18n"

export function LanguageSwitcher({ compact = false }) {
  const { language, setLanguage, t } = useI18n()

  return (
    <div className="flex items-center gap-1" aria-label={t("language")}>
      {languages.map((item) => (
        <button
          key={item.code}
          className={`grid h-9 w-9 place-items-center rounded-md border text-lg shadow-sm transition hover:border-signal ${language === item.code ? "border-signal bg-surface" : "border-line bg-panel"}`}
          type="button"
          onClick={() => setLanguage(item.code)}
          title={item.label}
          aria-label={item.label}
          aria-pressed={language === item.code}
        >
          <span aria-hidden="true">{item.flag}</span>
          {!compact && <span className="sr-only">{item.label}</span>}
        </button>
      ))}
    </div>
  )
}
