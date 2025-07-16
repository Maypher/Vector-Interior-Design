import type { MetadataRoute } from 'next'
import { getPayload } from 'payload'
import config from '@payload-config'
import { routing } from '@/i18n/routing'
import { AssertionError } from 'assert'
import { Media } from '@/payload-types'

// Forcing dynamic since by default this is cached at build time
// but because everything is dockerized the databased isn't accessible then
// and regardless the sitemap isn't the most accessed content so performance wise there
// shouldn't be issues.
export const dynamic = 'force-dynamic'

const baseURL = process.env.NEXT_PUBLIC_PAYLOAD_URL

function alternateUrls(path: string): { languages: Record<string, string> } | undefined {
  if (path.startsWith('/')) throw new AssertionError({ message: 'Only relative paths allowed' })
  if (!baseURL) return

  const languages: { languages: Record<string, string> } = {
    languages: {},
  }

  routing.locales.forEach((locale) => {
    languages.languages[locale] = `${baseURL}/${locale}/${path}`
  })

  return languages
}

async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const payload = await getPayload({ config })

  const mainPageLastModified = (
    await payload.findGlobal({
      slug: 'mainPageImages',
      overrideAccess: false,
      select: {
        updatedAt: true,
      },
    })
  ).updatedAt

  const projects = await payload.find({
    collection: 'project',
    overrideAccess: false,
    pagination: false,
    select: {
      updatedAt: true,
      _status: true,
      images: true,
      thumbnail: true,
    },
  })

  const sculptures = await payload.findGlobal({
    slug: 'sculpture',
    overrideAccess: false,
    select: {
      updatedAt: true,
    },
  })

  const conclusion = await payload.findGlobal({
    slug: 'conclusion',
    overrideAccess: false,
    select: {
      updatedAt: true,
    },
  })

  const sitemap: MetadataRoute.Sitemap = [
    {
      url: baseURL || '',
      alternates: alternateUrls(''),
      changeFrequency: 'yearly',
      priority: 1.0,
      lastModified: mainPageLastModified || undefined,
    },
    {
      url: `${baseURL}/projects`,
      alternates: alternateUrls('projects'),
      changeFrequency: 'yearly',
      priority: 0.8,
      // This iterates over all projects and gets the latest date a project was updated (be it the project itself or the thumbnail)
      lastModified: new Date(
        Math.max(
          ...projects?.docs.flatMap((project) => [
            new Date((project.updatedAt, project.thumbnail as Media)?.updatedAt).getTime(),
          ]),
        ),
      ),
    },
    {
      url: `${baseURL}/sculptures`,
      alternates: alternateUrls('sculptures'),
      priority: 0.6,
      changeFrequency: 'yearly',
      lastModified: sculptures.updatedAt || undefined,
    },
    {
      url: `${baseURL}/conclusion`,
      alternates: alternateUrls('conclusion'),
      changeFrequency: 'yearly',
      lastModified: conclusion.updatedAt || undefined,
      priority: 0.1,
    },
  ]

  projects?.docs.forEach((project) => {
    const path = `projects/${project.id}`
    sitemap.push({
      url: `${baseURL}/${path}`,
      alternates: alternateUrls(path),
      changeFrequency: 'yearly',
      priority: 0.4,
      lastModified: project.updatedAt,
      images: project.images?.flatMap((image) =>
        image.blockType === 'image'
          ? `${baseURL}${(image.image as Media).url!}`
          : image.blockType === 'imageGroup'
            ? image.images!.map((image) => `${baseURL}${(image.image as Media).url!}`)
            : '',
      ),
    })
  })

  return sitemap
}

export default sitemap
