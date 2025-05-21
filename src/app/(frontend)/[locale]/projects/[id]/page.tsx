import { getPayload } from 'payload'
import config from '@payload-config'
import { Project, Media } from '@/payload-types'
import RefreshRouterOnSave from '@/components/admin/RefreshRouteOnSave'
import { notFound } from 'next/navigation'
import Image from 'next/image'

import { headers as getHeaders } from 'next/headers'

interface Props {
  params: Promise<{
    locale: 'en' | 'es'
    id: number
  }>
}

const Page = async ({ params }: Props) => {
  const payload = await getPayload({ config })
  const { locale, id } = await params

  // Checking if the user is authenticated
  const headers = await getHeaders()
  const { user } = await payload.auth({ headers })

  const project: Project | null = await payload.findByID({
    collection: 'project',
    id,
    user,
    locale,
    depth: 2,
    draft: true, // Used for live preview. When an unauthenticated user access the site the published version will be returned
    overrideAccess: false,
    disableErrors: true, // Return null instead of throwing an error if the project doesn't exist
  })

  if (!project) notFound()

  return (
    <div>
      <RefreshRouterOnSave />
      <h1>{project.name}</h1>
    </div>
  )
}

export default Page
