import { useState } from "react"

import { api } from "../api/client"
import { AuthLayout } from "../components/AuthLayout"
import { useI18n } from "../i18n"

export function LoginPage({ onReady }) {
  const { t } = useI18n()
  const [form, setForm] = useState({ identifier: "", password: "" })
  const [error, setError] = useState("")
  const [busy, setBusy] = useState(false)

  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value })

  async function submit(event) {
    event.preventDefault()
    const identifier = form.identifier.trim()
    if (!identifier) {
      setError(t("auth.emailOrNameRequired"))
      return
    }
    if (!form.password) {
      setError(t("auth.passwordRequired"))
      return
    }
    setBusy(true)
    setError("")
    try {
      const user = await api.login({ ...form, identifier })
      onReady(user)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <AuthLayout subtitle={t("auth.loginSubtitle")}>
      <form className="space-y-4" onSubmit={submit} noValidate>
        <div>
          <label className="label" htmlFor="identifier">{t("auth.emailOrName")}</label>
          <input className="field mt-1" id="identifier" name="identifier" value={form.identifier} onChange={update} autoComplete="username" required />
        </div>
        <div>
          <label className="label" htmlFor="password">{t("auth.password")}</label>
          <input className="field mt-1" id="password" name="password" type="password" value={form.password} onChange={update} autoComplete="current-password" required />
        </div>
        {error && <p className="text-sm text-red-300">{error}</p>}
        <button className="btn-primary w-full" disabled={busy}>{busy ? t("auth.signingIn") : t("auth.login")}</button>
      </form>
    </AuthLayout>
  )
}
