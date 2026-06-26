import { ServerCog } from "lucide-react"

import { LanguageSwitcher } from "./LanguageSwitcher"
import { ThemeSwitcher } from "./ThemeSwitcher"

export function AuthLayout({ children, subtitle }) {
  return (
    <main className="grid min-h-screen place-items-center bg-surface px-4 py-8">
      <section className="w-full max-w-md rounded-lg border border-line bg-panel p-5 shadow-xl sm:p-7">
        <div className="mb-6 flex items-start justify-between gap-3">
          <div className="flex min-w-0 items-center gap-3">
            <div className="grid h-11 w-11 shrink-0 place-items-center rounded-md bg-signal text-white">
              <ServerCog size={24} aria-hidden="true" />
            </div>
            <div className="min-w-0">
              <h1 className="text-xl font-semibold text-ink">Jarvis Control Center</h1>
              <p className="text-sm text-muted">{subtitle}</p>
            </div>
          </div>
          <div className="flex shrink-0 flex-col items-end gap-2">
            <LanguageSwitcher compact />
            <ThemeSwitcher />
          </div>
        </div>
        {children}
      </section>
    </main>
  )
}
