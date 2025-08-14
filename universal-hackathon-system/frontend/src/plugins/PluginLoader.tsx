import { useEffect, useMemo, useState } from 'react'
import { Link, Route, Routes, useLocation } from 'react-router-dom'
import { api } from '../services/api'

const modules = import.meta.glob('./**/*.tsx')

export default function PluginLoader() {
  const [plugins, setPlugins] = useState<any[]>([])
  const location = useLocation()

  useEffect(() => {
    api.get('/plugins').then(r => setPlugins(r.data)).catch(() => setPlugins([]))
  }, [])

  const routes = useMemo(() => {
    return plugins.map(p => {
      const name = p.name
      const entry = p.frontend?.entry as string
      const importer = modules[`./${name}/frontend.tsx`] || modules[`../${entry}` as any]
      const Component = (props: any) => {
        const [C, setC] = useState<any>(null)
        useEffect(() => { importer().then((m: any) => setC(() => m.default)) }, [])
        if (!importer) return <div>Plugin component not found</div>
        return C ? <C {...props} /> : <div>Loading...</div>
      }
      return { name, path: `/plugins/${name}`, Component }
    })
  }, [plugins])

  return (
    <div>
      <div className="mb-3 flex gap-3">
        {routes.map(r => (
          <Link key={r.name} to={r.path} className={location.pathname === r.path ? 'underline' : ''}>{r.name}</Link>
        ))}
        {routes.length === 0 && <span className="text-sm text-slate-500">No plugins enabled</span>}
      </div>
      <Routes>
        {routes.map(r => <Route key={r.name} path={r.name} element={<r.Component />} />)}
      </Routes>
    </div>
  )
}