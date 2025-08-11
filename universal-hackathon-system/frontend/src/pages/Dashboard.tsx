import { useEffect, useMemo, useState } from 'react'
import { api } from '../services/api'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

export default function Dashboard() {
  const [stats, setStats] = useState<any>({ by_minute: {} })
  const [events, setEvents] = useState<any[]>([])

  useEffect(() => {
    api.get('/events/stats').then(r => setStats(r.data))
    api.get('/events').then(r => setEvents(r.data))
  }, [])

  const data = useMemo(() => {
    const entries = Object.entries(stats.by_minute || {}) as [string, number][]
    return entries.sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => ({ time: k.slice(11, 16), value: v }))
  }, [stats])

  return (
    <div className="space-y-6">
      <div className="bg-white border rounded p-3 h-64">
        <h3 className="font-semibold mb-2">Events over time</h3>
        <ResponsiveContainer width="100%" height="90%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#0ea5e9" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white border rounded p-3">
        <h3 className="font-semibold mb-2">Recent events</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left border-b">
                <th className="py-2">ID</th>
                <th>Type</th>
                <th>Message</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {events.map(e => (
                <tr key={e.id} className="border-b last:border-0">
                  <td className="py-2">{e.id}</td>
                  <td>{e.type}</td>
                  <td className="max-w-[400px] truncate">{e.payload?.message}</td>
                  <td>{new Date(e.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}