'use client'

import Image from 'next/image'
import logoWhite from '@public/images/logoWhite.svg'

export default function Footer() {
  return (
    <div>
      <div className="relative flex flex-wrap items-center justify-center gap-x-5 px-2 py-20 bg-vector-black">
        <p className="border-vector-orange border-b-1 xs:border-b-0 xs:border-r-1 py-2 xs:pr-5 text-2xl">
          Contacto
        </p>
        <a href="mailto:contact@vectorinterior.design" className="py-5">
          contact@vectorinterior.design
        </a>
      </div>
      <div className="bg-vector-grey flex h-24 justify-center p-6">
        <button
          className="hover:scale-120 h-full cursor-pointer transition-transform"
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        >
          <Image alt="vector: Interior Design" className="h-full" src={logoWhite} />
        </button>
      </div>
    </div>
  )
}
