import { withPayload } from '@payloadcms/next/withPayload'
import createNextIntlPlugin from 'next-intl/plugin'

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    imageSizes: [800, 1500, 1920],
  },
  devIndicators: {
    position: 'bottom-right',
  },
}

const withNextIntl = createNextIntlPlugin()
export default withNextIntl(withPayload(nextConfig, { devBundleServerPackages: false }))
