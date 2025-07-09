'use client'
import { useTranslations } from 'next-intl'
import { Link } from '@/i18n/navigation'

export default function NotFound() {
  const t = useTranslations('errors')

  return (
    <div className="header-screen p-2 flex flex-col gap-10 items-center justify-center">
      <h1 className="text-center">{t('404')}</h1>
      <Link href="/" className="text-4xl">
        &lt;
      </Link>
    </div>
  )
}
