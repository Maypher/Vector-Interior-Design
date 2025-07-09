import fs from 'node:fs'

function readSecret(path: string, fallback: string = ''): string {
  try {
    return fs.readFileSync(path).toString()
  } catch {
    return fallback || ''
  }
}

// Secrets loaded from files because they're inserted at build time by docker secrets
// If no secret is found then read it from an environment variable (Mostly to allow for migrations and running node locally)
export const PAYLOAD_SECRET = readSecret('/run/secrets/payload-secret', process.env.PAYLOAD_SECRET)

export const DATABASE_URI =
  process.env.DATABASE_URI ||
  `postgres://postgres:${readSecret('/run/secrets/postgres-password')}@postgres:5432/postgres`
export const EMAIL_PASSWORD = readSecret('/run/secrets/email-password', process.env.EMAIL_PASSWORD)
