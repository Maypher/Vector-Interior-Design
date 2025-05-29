import { Media } from '@/payload-types'
import Image from 'next/image'
import '@styles/skeleton.scss'

interface Props {
  image: Media
  className?: string
}

export default function ImageSkeleton({ image, className }: Props) {
  return (
    <Image
      src={image.url!}
      alt={image.alt}
      width={image.width!}
      height={image.height!}
      placeholder="blur"
      blurDataURL={image.sizes!.loading!.url!}
      className={`h-full w-auto object-contain ${className}`}
    />
  )
}
