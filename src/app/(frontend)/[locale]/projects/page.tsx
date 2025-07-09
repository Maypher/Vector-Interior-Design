import { getPayload } from 'payload'
import config from '@/payload.config'
import Carousel from '@/components/carousel'
import { Suspense } from 'react'
import { draftMode } from 'next/headers'
import RefreshRouteOnSave from '@/components/admin/RefreshRouteOnSave'
import { Metadata } from 'next'
import { getTranslations, setRequestLocale } from 'next-intl/server'
import { Media } from '@/payload-types'

export const dynamic = 'error'

export default async function Page({ params }: { params: Promise<{ locale: 'es' | 'en' }> }) {
  const { isEnabled } = await draftMode()
  const payload = await getPayload({ config })
  const { locale } = await params

  const projects = await payload.find({
    collection: 'project',
    select: {
      name: true,
      thumbnail: true,
      _status: true,
    },
    locale,
    draft: isEnabled,
    overrideAccess: isEnabled,
  })

  if (projects.docs.length === 0)
    return <div className="grow flex items-center justify-center">No projects to show</div>

  return (
    <Suspense>
      <Carousel projects={projects.docs} />
      {isEnabled && <RefreshRouteOnSave />}
    </Suspense>
  )
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>
}): Promise<Metadata> {
  const { locale } = await params

  setRequestLocale(locale)

  const t = await getTranslations({ locale })
  const title = t('NavBar.projects')

  const payload = await getPayload({ config })

  const data = await payload.find({
    collection: 'project',
    locale: locale as 'es' | 'en',
    select: {
      thumbnail: true,
    },
  })

  const ogImage = data.docs.at(0)?.thumbnail as Media

  return {
    metadataBase: new URL(process.env.NEXT_PUBLIC_PAYLOAD_URL || ''),
    title,
    openGraph: {
      images: ogImage.url!,
    },
  }
}
