import { FormEvent, useState } from 'react'
import { api } from '../services/api'
import { Link, useNavigate } from 'react-router-dom'

export default function Register() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('test@example.com')
  const [password, setPassword] = useState('secret')
  const [error, setError] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      await api.post('/auth/register', { email, password })
      navigate('/login')
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Register failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={onSubmit} className="bg-white border rounded p-6 w-96 space-y-3">
        <h1 className="text-xl font-semibold">Register</h1>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <input className="w-full border rounded p-2" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full border rounded p-2" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="w-full bg-slate-800 text-white rounded p-2">Create account</button>
        <div className="text-sm">
          Already have an account? <Link className="underline" to="/login">Login</Link>
        </div>
      </form>
    </div>
  )
}