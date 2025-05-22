'use client'

import { Media } from '@/payload-types'
import { useState } from 'react'
import Image from 'next/image'
import '@styles/skeleton.scss'

interface Props {
  image: Media
  onLoad?: () => void
}

export default function ImageSkeleton({ image }: Props) {
  return (
    <Image
      src={image.url!}
      alt={image.alt}
      width={image.width!}
      height={image.height!}
      placeholder="blur"
      blurDataURL={image.sizes!.loading!.url!}
      className="h-full w-auto object-contain"
    />
  )
}
