import { withPayload } from '@payloadcms/next/withPayload'

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    imageSizes: [800, 1500, 1920],
  },
  devIndicators: {
    position: 'bottom-right',
  },
}

export default withPayload(nextConfig, { devBundleServerPackages: false })
