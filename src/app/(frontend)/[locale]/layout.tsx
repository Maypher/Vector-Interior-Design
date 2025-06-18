import '../globals.css'
import Header from '@/components/global/Header'
import { nexaFont } from '@styles/fonts'

import { NextIntlClientProvider, hasLocale } from 'next-intl'
import { routing } from '@/i18n/routing'
import { notFound } from 'next/navigation'
import { setRequestLocale } from 'next-intl/server'
import { DraftMode } from '@/components/global/DraftMode'
import { draftMode } from 'next/headers'

export default async function RootLayout(props: {
  children: React.ReactNode
  params: Promise<{ locale: string }>
}) {
  const { children, params } = props

  // Ensure that the incoming `locale` is valid
  const { locale } = await params
  if (!hasLocale(routing.locales, locale)) {
    notFound()
  }

  setRequestLocale(locale)

  const { isEnabled } = await draftMode()

  return (
    <html>
      <body
        style={{ scrollbarGutter: 'stable', overflowY: 'scroll' }}
        className={`${nexaFont.className} text-vector-cream bg-vector-black min-h-svh flex flex-col`}
      >
        <NextIntlClientProvider>
          <Header />
          <main className="grow flex flex-col">{children}</main>
        </NextIntlClientProvider>
        {isEnabled && <DraftMode />}
      </body>
    </html>
  )
}
