'use client'

import '@styles/nav.scss'

import Image from '@/components/global/Image'
import symbol from '@public/images/symbol.svg'
import { useEffect } from 'react'

export default function NavLinks() {
  useEffect(() => {
    // This entire setup doesn't work in Chrome mobile app for some reason
    const pencilObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const pencil = document.getElementById('pencil')
            if (pencil) {
              pencil.classList.add('pencil-animate')
              pencilObserver.unobserve(entry.target)
            }
          }
        })
      },
      {
        threshold: 0.6,
      },
    )

    const pencil = document.getElementById('nav')
    if (pencil) pencilObserver.observe(pencil)
  })

  return (
    <div className="h-92 flex w-[2px] flex-col items-center overflow-visible" id="pencil">
      <Image alt="V" className="min-h-20 min-w-20" src={symbol} />
      <div className="bg-vector-orange relative bottom-3 h-2/3 w-px"></div>
    </div>
  )
}
