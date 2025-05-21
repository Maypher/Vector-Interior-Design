import '../globals.css'
import Image from 'next/image'
import logo from '@public/images/logo.svg'

import LanguageSelect from '@/components/global/LanguageSelect'
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
        className="font-Nexa text-vector-cream"
      >
        {user && (
          <p className="fixed top-5 right-5 bg-vector-black/50 p-2">Viendo previsualización.</p>
        )}
        <NextIntlClientProvider>
          <header className="h-22 bg-vector-cream px-10 py-5 flex items-center justify-between">
            <Image src={logo} alt="Vector: Interior Design" className="h-full w-fit" />
            <div className="hidden xl:block">
              <LanguageSelect />
            </div>
          </header>
          <main>{children}</main>
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
