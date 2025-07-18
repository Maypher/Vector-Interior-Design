import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      disallow: '/admin/',
    },
    sitemap: `${process.env.NEXT_PUBLIC_PAYLOAD_URL}/sitemap.xml`,
  }
}
