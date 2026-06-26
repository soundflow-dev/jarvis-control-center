import { Activity, FolderOpen, LogOut, ServerCog, Settings, TerminalSquare } from "lucide-react"

import { useI18n } from "../i18n"
import { LanguageSwitcher } from "./LanguageSwitcher"
import { ThemeSwitcher } from "./ThemeSwitcher"

export function Shell({ user, onLogout, children }) {
  const { t } = useI18n()

  return (
    <div className="min-h-screen bg-surface">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-12 border-r border-line bg-panel md:flex md:flex-col md:items-center">
        <div className="grid h-14 w-full place-items-center border-b border-line">
          <span className="h-1.5 w-1.5 rounded-full bg-green-500" />
        </div>
        <nav className="flex flex-1 flex-col items-center gap-1 py-3 text-muted" aria-label="Jarvis navigation">
          <button className="grid h-9 w-9 place-items-center rounded-md bg-signal/10 text-signal" type="button" title="Dashboard">
            <Activity size={18} aria-hidden="true" />
          </button>
          <button className="grid h-9 w-9 place-items-center rounded-md hover:bg-surface hover:text-ink" type="button" title={t("common.files")}>
            <FolderOpen size={18} aria-hidden="true" />
          </button>
          <button className="grid h-9 w-9 place-items-center rounded-md hover:bg-surface hover:text-ink" type="button" title={t("common.terminal")}>
            <TerminalSquare size={18} aria-hidden="true" />
          </button>
        </nav>
        <div className="flex flex-col items-center gap-1 border-t border-line py-3 text-muted">
          <button className="grid h-9 w-9 place-items-center rounded-md hover:bg-surface hover:text-ink" type="button" title="Settings">
            <Settings size={18} aria-hidden="true" />
          </button>
        </div>
      </aside>

      <div className="md:pl-12">
        <header className="sticky top-0 z-10 border-b border-line bg-panel/95 backdrop-blur">
          <div className="flex h-14 items-center justify-between gap-3 px-4 sm:px-6">
            <div className="flex min-w-0 items-center gap-3">
              <div className="grid h-9 w-9 shrink-0 place-items-center rounded bg-signal text-white">
                <ServerCog size={20} aria-hidden="true" />
              </div>
              <div className="min-w-0">
                <p className="truncate text-sm font-semibold text-ink">Jarvis Control Center</p>
                <p className="truncate text-xs text-muted">{user?.name}</p>
              </div>
            </div>
            <p className="pointer-events-none hidden select-none text-sm font-semibold text-muted/30 lg:block">Jarvis</p>
            <div className="flex shrink-0 items-center gap-2">
              <LanguageSwitcher compact />
              <ThemeSwitcher />
              <button className="btn-secondary px-3" onClick={onLogout} title={t("logout")}>
                <LogOut size={17} aria-hidden="true" />
                <span className="hidden sm:inline">{t("logout")}</span>
              </button>
            </div>
          </div>
        </header>
        <main className="px-3 py-4 sm:px-4 lg:px-5">{children}</main>
      </div>
    </div>
  )
}
