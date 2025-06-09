'use client'
import Image from 'next/image'
import logoWhite from '@public/images/logoWhite.svg'

export default function ScrollToTop({ backgroundColor }: { backgroundColor: string }) {
  return (
    <div className="flex justify-center pb-10" style={{ backgroundColor }}>
      <button
        type="button"
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        className="h-11"
      >
        <Image
          src={logoWhite}
          alt="Vector: Interior Design"
          className="h-full w-fit cursor-pointer transition-transform hover:scale-115"
        />
      </button>
    </div>
  )
}
