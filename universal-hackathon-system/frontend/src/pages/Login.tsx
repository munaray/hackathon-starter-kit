import { FormEvent, useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { Link, useLocation, useNavigate } from 'react-router-dom'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation() as any
  const from = location.state?.from?.pathname || '/'
  const [email, setEmail] = useState('test@example.com')
  const [password, setPassword] = useState('secret')
  const [error, setError] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      await login(email, password)
      navigate(from, { replace: true })
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={onSubmit} className="bg-white border rounded p-6 w-96 space-y-3">
        <h1 className="text-xl font-semibold">Login</h1>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <input className="w-full border rounded p-2" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full border rounded p-2" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="w-full bg-slate-800 text-white rounded p-2">Sign in</button>
        <div className="text-sm">
          No account? <Link className="underline" to="/register">Register</Link>
        </div>
      </form>
    </div>
  )
}