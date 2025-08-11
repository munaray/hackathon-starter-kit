export function createWS(path: string) {
  const base = (import.meta.env.VITE_WS_URL || 'ws://localhost:8000')
  return new WebSocket(`${base}${path}`)
}