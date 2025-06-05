import { Media } from '@/payload-types'
import Image from 'next/image'
import '@styles/skeleton.scss'
import { CSSProperties } from 'react'

interface Props {
  image: Media
  className?: string
  style?: CSSProperties
  sizes?: string
}

export default function ImageSkeleton({ image, className, style, sizes }: Props) {
  return (
    <Image
      src={image.url!}
      alt={image.alt}
      width={image.width!}
      height={image.height!}
      placeholder="blur"
      blurDataURL={image.sizes!.loading!.url!}
      sizes={sizes}
      className={`h-full w-auto object-contain ${className}`}
      style={style}
    />
  )
}
