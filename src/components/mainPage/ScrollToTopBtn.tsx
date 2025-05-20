'use client'

import Image from 'next/image'

import '@styles/descriptions.scss'
import logoWhite from '@public/images/logoWhite.svg'

export default function ScrollToTopBtn() {
  return (
    <button
      type="button"
      onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
      className="absolute bottom-20 right-20 h-11"
    >
      <Image
        src={logoWhite}
        alt="Vector: Interior Design"
        className="h-full w-fit cursor-pointer transition-transform hover:scale-115"
      />
    </button>
  )
}
