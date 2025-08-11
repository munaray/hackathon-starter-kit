import { useEffect, useState } from 'react'
import { api } from '../../services/api'

export default function CustomerOnboardingPlugin() {
  const [data, setData] = useState<any>(null)
  useEffect(() => {
    api.get('/plugins/customer_onboarding/status').then(r => setData(r.data))
  }, [])
  return (
    <div className="bg-white border rounded p-3">
      <h3 className="font-semibold mb-2">Customer Onboarding</h3>
      <pre className="text-xs">{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}