import '../globals.css'
import Image from 'next/image'
import logo from '@public/images/logo.svg'

import LanguageSelect from '@components/LanguageSelect'
import { NextIntlClientProvider, hasLocale } from 'next-intl'
import { routing } from '@/i18n/routing'
import { notFound } from 'next/navigation'

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

  return (
    <html>
      <body>
        <NextIntlClientProvider>
          <header className="h-22 bg-vector-cream px-10 py-5 flex items-center justify-between">
            <Image src={logo} alt="Vector: Interior Design" className="h-full w-fit" />
            <LanguageSelect />
          </header>
          <main>{children}</main>
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
