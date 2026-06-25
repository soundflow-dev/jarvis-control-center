import { useState } from "react"
import { AlertTriangle } from "lucide-react"

import { api } from "../api/client"
import { AuthLayout } from "../components/AuthLayout"
import { useI18n } from "../i18n"

export function SetupPage({ status, onReady }) {
  const { t } = useI18n()
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm_password: "" })
  const [error, setError] = useState("")
  const [busy, setBusy] = useState(false)

  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value })

  async function submit(event) {
    event.preventDefault()
    const name = form.name.trim()
    const email = form.email.trim()
    if (!name) {
      setError(t("auth.nameRequired"))
      return
    }
    if (!form.password) {
      setError(t("auth.passwordRequired"))
      return
    }
    if (!form.confirm_password) {
      setError(t("auth.passwordConfirmationRequired"))
      return
    }
    if (form.password !== form.confirm_password) {
      setError(t("auth.passwordsDoNotMatch"))
      return
    }
    setBusy(true)
    setError("")
    try {
      const payload = { ...form, name, email: email || null }
      const user = await api.setup(payload)
      onReady(user)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <AuthLayout subtitle={t("auth.setupSubtitle")}>
      {status?.warning && (
        <div className="mb-4 flex gap-3 rounded-md border border-warning/40 bg-warning/10 p-3 text-sm text-amber-100">
          <AlertTriangle className="mt-0.5 shrink-0" size={18} aria-hidden="true" />
          <span>{status.warning}</span>
        </div>
      )}
      <form className="space-y-4" onSubmit={submit} noValidate>
        <div>
          <label className="label" htmlFor="name">{t("auth.name")}</label>
          <input className="field mt-1" id="name" name="name" value={form.name} onChange={update} autoComplete="name" required />
        </div>
        <div>
          <label className="label" htmlFor="email">{t("auth.emailOptional")}</label>
          <input className="field mt-1" id="email" name="email" type="email" value={form.email} onChange={update} autoComplete="email" />
        </div>
        <div>
          <label className="label" htmlFor="password">{t("auth.password")}</label>
          <input className="field mt-1" id="password" name="password" type="password" value={form.password} onChange={update} autoComplete="new-password" required />
        </div>
        <div>
          <label className="label" htmlFor="confirm_password">{t("auth.confirmPassword")}</label>
          <input className="field mt-1" id="confirm_password" name="confirm_password" type="password" value={form.confirm_password} onChange={update} autoComplete="new-password" required />
        </div>
        {error && <p className="text-sm text-red-300">{error}</p>}
        <button className="btn-primary w-full" disabled={busy}>{busy ? t("auth.creating") : t("auth.createAdministrator")}</button>
      </form>
    </AuthLayout>
  )
}
