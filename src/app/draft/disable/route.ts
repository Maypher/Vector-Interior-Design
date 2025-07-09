import { draftMode } from 'next/headers'

export async function GET(_: Request) {
  const draft = await draftMode()

  draft.disable()

  return new Response('Draft mode disabled')
}
