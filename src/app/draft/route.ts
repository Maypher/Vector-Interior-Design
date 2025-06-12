import { redirect } from 'next/navigation'
import { draftMode } from 'next/headers'
import { getPayload } from 'payload'
import config from '@payload-config'

export async function GET(request: Request) {
  // Parse query string parameters
  const { searchParams } = new URL(request.url)
  const secret = searchParams.get('secret')
  const path = searchParams.get('path')

  if (secret !== process.env.DRAFT_MODE_SECRET || !path)
    return new Response('Invalid params', { status: 401 })

  const payload = await getPayload({ config })
  const { user } = await payload.auth({ headers: request.headers })

  if (!user) return new Response('Not authenticated', { status: 401 })

  const draft = await draftMode()
  draft.enable()
  redirect(path)
}
