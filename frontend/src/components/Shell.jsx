import { LogOut, ServerCog } from "lucide-react"

export function Shell({ user, onLogout, children }) {
  return (
    <div className="min-h-screen bg-surface">
      <header className="sticky top-0 z-10 border-b border-line bg-surface/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3 sm:px-6 lg:px-8">
          <div className="flex min-w-0 items-center gap-3">
            <div className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-signal text-slate-950">
              <ServerCog size={22} aria-hidden="true" />
            </div>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-ink">Jarvis Control Center</p>
              <p className="truncate text-xs text-muted">{user?.name}</p>
            </div>
          </div>
          <button className="btn-secondary px-3 sm:px-4" onClick={onLogout} title="Logout">
            <LogOut size={18} aria-hidden="true" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
    </div>
  )
}
