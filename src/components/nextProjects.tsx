'use client'

import { Link } from '@/i18n/navigation'
import { useTranslations } from 'next-intl'
import { useEffect, useRef } from 'react'

export default function NextProject({ next }: { next: number | 'conclusion' }) {
  const t = useTranslations('Project')

  const nextLink = useRef<HTMLAnchorElement>(null)

  const lastProject = next === 'conclusion'

  useEffect(() => {
    const intersectionObserver = new IntersectionObserver(
      (elements) => {
        if (elements.at(0)?.isIntersecting) nextLink.current?.classList.add('visible')
      },
      {
        threshold: 1,
      },
    )

    intersectionObserver.observe(document.getElementById('next-link')!)

    return () => intersectionObserver.disconnect()
  })

  return (
    <Link
      href={lastProject ? '/conclusion' : `/projects/${next}`}
      id="next-link"
      ref={nextLink}
      className="text-2xl border-1 border-vector-cream p-2 font-bold"
    >
      {t('next')}
    </Link>
  )
}
