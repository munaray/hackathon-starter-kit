import { Link, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import Dashboard from './pages/Dashboard'
import NotificationPanel from './components/NotificationPanel'
import PluginLoader from './plugins/PluginLoader'
import { useAuth } from './hooks/useAuth'

export default function App() {
  const { user, logout } = useAuth()
  return (
    <div className="min-h-screen">
      <header className="flex items-center justify-between px-6 py-3 border-b bg-white">
        <nav className="flex gap-4">
          <Link to="/">Dashboard</Link>
          <Link to="/plugins">Plugins</Link>
        </nav>
        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="text-sm text-slate-600">{user.email}</span>
              <button className="px-3 py-1 rounded bg-slate-200" onClick={logout}>Logout</button>
            </>
          ) : (
            <Link to="/login" className="px-3 py-1 rounded bg-slate-200">Login</Link>
          )}
        </div>
      </header>
      <main className="p-6 grid grid-cols-12 gap-6">
        <section className="col-span-9">
          <Routes>
            <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/plugins/*" element={<ProtectedRoute><PluginLoader /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </section>
        <aside className="col-span-3">
          <ProtectedRoute>
            <NotificationPanel />
          </ProtectedRoute>
        </aside>
      </main>
    </div>
  )
}