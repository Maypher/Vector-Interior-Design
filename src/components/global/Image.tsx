import ReactImage from 'next/image'
import '@styles/skeleton.scss'

type ImageProps = React.ComponentPropsWithoutRef<typeof ReactImage>

/**
 * This wrapper around Next's `Image` component that
 * removes the website's hostname (Indicated by `process.env.NEXT_PUBLIC_PAYLOAD_URL`)
 * from an image URL so that it becomes relative to avoid issues with remotePatterns and docker containers.
 * It accepts all the props `Image` accepts and does src.replace(process.env.NEXT_PUBLIC_PAYLOAD_URL || '', '')
 * to remove the hostname.
 */
export default function Image({ ...props }: ImageProps) {
  return (
    <ReactImage
      {...props}
      src={
        typeof props.src === 'string'
          ? props.src.replace(process.env.NEXT_PUBLIC_PAYLOAD_URL || '', '')
          : props.src
      }
      blurDataURL={props.blurDataURL?.replace(process.env.NEXT_PUBLIC_PAYLOAD_URL || '', '')}
    />
  )
}
