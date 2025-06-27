import fs from 'node:fs'

// Secrets loaded from files because they're inserted at build time by docker secrets
// If no secret is found then read it from an environment variable (Mostly to allow for migrations and running node locally)
export const PAYLOAD_SECRET = (() => {
  try {
    return fs.readFileSync('/run/secrets/payload-secret').toString()
  } catch {
    return process.env.PAYLOAD_SECRET || ''
  }
})()

export const DATABASE_URI = (() => {
  try {
    const password = fs.readFileSync('/run/secrets/postgres-password').toString()
    return `postgres://postgres:${password}@postgres:5432/postgres`
  } catch {
    return process.env.DATABASE_URI || ''
  }
})()
