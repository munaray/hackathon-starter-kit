import { useEffect, useState } from 'react'
import { api } from '../../services/api'

export default function TransactionReliabilityPlugin() {
  const [data, setData] = useState<any>(null)
  useEffect(() => {
    api.get('/plugins/transaction_reliability/reliability').then(r => setData(r.data))
  }, [])
  return (
    <div className="bg-white border rounded p-3">
      <h3 className="font-semibold mb-2">Transaction Reliability</h3>
      <pre className="text-xs">{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}