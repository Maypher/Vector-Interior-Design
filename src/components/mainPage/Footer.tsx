'use client'

import Image from 'next/image'
import logoWhite from '@public/images/logoWhite.svg'

export default function Footer() {
  return (
    <div className="bg-vector-grey flex h-24 justify-center p-6">
      <button
        className="hover:scale-120 h-full cursor-pointer transition-transform"
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
      >
        <Image alt="vector: Interior Design" className="h-full" src={logoWhite} />
      </button>
    </div>
  )
}
