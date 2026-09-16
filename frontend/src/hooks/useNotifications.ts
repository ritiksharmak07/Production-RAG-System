import { useState } from 'react'

export interface Notification {
  id: string
  message: string
  type: 'success' | 'error' | 'info'
}

export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([])

  const pushNotification = (message: string, type: Notification['type'] = 'info') => {
    const id = crypto.randomUUID()
    setNotifications((prev) => [...prev, { id, message, type }])
    window.setTimeout(() => {
      setNotifications((prev) => prev.filter((notification) => notification.id !== id))
    }, 5000)
  }

  return {
    notifications,
    pushNotification,
  }
}
