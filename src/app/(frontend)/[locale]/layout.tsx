import '../globals.css'
import Header from '@/components/global/Header'
import { nexaFont } from '@styles/fonts'
import { Metadata } from 'next'

import { NextIntlClientProvider, hasLocale } from 'next-intl'
import { routing } from '@/i18n/routing'
import { notFound } from 'next/navigation'
import { setRequestLocale } from 'next-intl/server'
import { DraftMode } from '@/components/global/DraftMode'
import { draftMode } from 'next/headers'
import { getTranslations } from 'next-intl/server'

interface Props {
  children: React.ReactNode
  params: Promise<{ locale: string }>
}

export default async function RootLayout(props: Props) {
  const { children, params } = props

  // Ensure that the incoming `locale` is valid
  const { locale } = await params
  if (!hasLocale(routing.locales, locale)) notFound()

  setRequestLocale(locale)

  const { isEnabled } = await draftMode()

  return (
    <html lang={locale}>
      <body
        style={{ scrollbarGutter: 'stable', overflowY: 'scroll' }}
        className={`${nexaFont.className} text-vector-cream bg-vector-black min-h-svh flex flex-col overflow-x-clip`}
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

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params

  const t = await getTranslations({ namespace: 'Metadata', locale })

  return {
    metadataBase: new URL(process.env.NEXT_PUBLIC_PAYLOAD_URL || ''),
    title: {
      template: '%s | Vector',
      default: 'Vector: Interior Design',
    },
    description: t('google'),
    openGraph: {
      url: process.env.NEXT_PUBLIC_PAYLOAD_URL,
      siteName: 'Vector: Interior Design',
    },
  }
}
