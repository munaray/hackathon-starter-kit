import { useEffect, useState } from 'react'
import { api } from '../services/api'

export default function NotificationPanel() {
  const [items, setItems] = useState<any[]>([])
  useEffect(() => {
    api.get('/notify/inapp').then(r => setItems(r.data)).catch(() => setItems([]))
  }, [])
  return (
    <div className="bg-white rounded border p-3">
      <h3 className="font-semibold mb-2">Notifications</h3>
      <div className="space-y-2">
        {items.map(n => (
          <div key={n.id} className="p-2 rounded border">
            <div className="text-sm font-medium">{n.title}</div>
            <div className="text-xs text-slate-600">{n.message}</div>
          </div>
        ))}
        {items.length === 0 && <div className="text-sm text-slate-500">No notifications</div>}
      </div>
    </div>
  )
}