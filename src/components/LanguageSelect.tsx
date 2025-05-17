'use client'

import clsx from 'clsx'
import { useParams } from 'next/navigation'
import { Locale, useTranslations } from 'next-intl'
import { ChangeEvent, useTransition } from 'react'
import { usePathname, useRouter } from '@/i18n/navigation'
import { routing } from '@/i18n/routing'

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
      className="inline-flex appearance-none bg-transparent py-3 pl-2 pr-6"
      defaultValue="en"
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
