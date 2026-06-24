import { ServerCog } from "lucide-react"

export function AuthLayout({ children, subtitle }) {
  return (
    <main className="grid min-h-screen place-items-center bg-surface px-4 py-8">
      <section className="w-full max-w-md rounded-lg border border-line bg-panel p-5 shadow-2xl shadow-black/30 sm:p-7">
        <div className="mb-6 flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-md bg-signal text-slate-950">
            <ServerCog size={24} aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-ink">Jarvis Control Center</h1>
            <p className="text-sm text-muted">{subtitle}</p>
          </div>
        </div>
        {children}
      </section>
    </main>
  )
}
