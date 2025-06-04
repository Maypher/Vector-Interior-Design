import { getPayload } from 'payload'
import config from '@/payload.config'
import { headers } from 'next/headers'
import Carousel from '@/components/carousel'

export default async function Page() {
  const reqHeaders = await headers()
  const payload = await getPayload({ config })
  const { user } = await payload.auth({ headers: reqHeaders })

  const projects = await payload.find({
    collection: 'project',
    user,
    select: {
      name: true,
      thumbnail: true,
    },
    overrideAccess: false,
    disableErrors: true,
    draft: Boolean(user),
  })

  return <Carousel projects={projects.docs} />
}
