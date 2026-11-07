type ErrorNotifier = (message: string) => void

const DEDUPE_WINDOW_MS = 3000

let notifier: ErrorNotifier | null = null
let lastMessage = ''
let lastNotifiedAt = 0

export function setErrorNotifier(next: ErrorNotifier | null): void {
  notifier = next
}

export function notifyError(message: string): void {
  if (notifier === null) {
    return
  }

  const now = Date.now()
  if (message === lastMessage && now - lastNotifiedAt < DEDUPE_WINDOW_MS) {
    return
  }

  lastMessage = message
  lastNotifiedAt = now
  notifier(message)
}
