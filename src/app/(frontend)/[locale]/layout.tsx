import '../globals.css'
import Header from '@/components/global/Header'
import { nexaFont } from '@styles/fonts'

import { NextIntlClientProvider, hasLocale } from 'next-intl'
import { routing } from '@/i18n/routing'
import { notFound } from 'next/navigation'
import { getPayload } from 'payload'
import config from '@/payload.config'
import { headers } from 'next/headers'

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

  const payload = await getPayload({ config })
  const { user } = await payload.auth({ headers: await headers() })

  return (
    <html>
      <body
        style={{ scrollbarGutter: 'stable', overflowY: 'scroll' }}
        className={`${nexaFont.className} text-vector-cream bg-vector-black`}
      >
        {user && (
          <p className="fixed top-5 right-5 bg-vector-black/50 p-2 pointer-events-none opacity-20">
            Viendo previsualización.
          </p>
        )}
        <NextIntlClientProvider>
          <Header />
          <main>{children}</main>
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
