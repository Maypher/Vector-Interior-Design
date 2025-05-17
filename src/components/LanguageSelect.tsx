'use client'

import { useParams } from 'next/navigation'
import { Locale, useTranslations } from 'next-intl'
import { ChangeEvent, useTransition } from 'react'
import { usePathname, useRouter } from '@/i18n/navigation'
import { routing } from '@/i18n/routing'
import { nexaFont } from '@styles/fonts'

export default function LocaleSwitcherSelect() {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()
  const pathname = usePathname()
  const params = useParams()
  const t = useTranslations('LocaleSwitcher')

  function onSelectChange(event: ChangeEvent<HTMLSelectElement>) {
    const nextLocale = event.target.value as Locale
    startTransition(() => {
      router.replace(
        // @ts-expect-error -- TypeScript will validate that only known `params`
        // are used in combination with a given `pathname`. Since the two will
        // always match for the current route, we can skip runtime checks.
        { pathname, params },
        { locale: nextLocale },
      )
    })
  }

  return (
    <select
      className={`${nexaFont.className} xl:text-vector-black pr-1`}
      defaultValue={params.locale}
      disabled={isPending}
      onChange={onSelectChange}
    >
      {routing.locales.map((cur) => (
        <option key={cur} value={cur}>
          {t('locale', { locale: cur })}
        </option>
      ))}
    </select>
  )
}
