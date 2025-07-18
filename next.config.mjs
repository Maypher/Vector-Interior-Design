import { withPayload } from '@payloadcms/next/withPayload'
import createNextIntlPlugin from 'next-intl/plugin'

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    deviceSizes: [640, 750, 828, 1024, 1280, 1440, 1920, 2048, 3840],
    formats: ['image/webp'],
  },
  devIndicators: {
    position: 'bottom-right',
  },
  output: 'standalone',
  experimental: {
    serverActions: {
      allowedOrigins: ['payload:3000', 'localhost:1000', process.env.DOMAIN],
    },
  },
}

const withNextIntl = createNextIntlPlugin()
export default withNextIntl(withPayload(nextConfig, { devBundleServerPackages: false }))
