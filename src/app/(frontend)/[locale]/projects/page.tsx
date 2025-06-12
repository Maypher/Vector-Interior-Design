import { getPayload } from 'payload'
import config from '@/payload.config'
import Carousel from '@/components/carousel'
import { Suspense } from 'react'
import { draftMode } from 'next/headers'
import RefreshRouteOnSave from '@/components/admin/RefreshRouteOnSave'

export default async function Page() {
  const { isEnabled } = await draftMode()
  const payload = await getPayload({ config })

  const projects = await payload.find({
    collection: 'project',
    select: {
      name: true,
      thumbnail: true,
      _status: true,
    },
    draft: isEnabled,
    overrideAccess: isEnabled,
  })

  if (projects.docs.length === 0)
    return <div className="grow flex items-center justify-center">No projects to show</div>

  return (
    <Suspense>
      <RefreshRouteOnSave />
      <Carousel projects={projects.docs} />
    </Suspense>
  )
}
