import { NextRequest, NextResponse } from 'next/server'
import { match } from '@formatjs/intl-localematcher'
import Negotiator from 'negotiator'

const locales = ['en', 'es']

function getLocale(request: NextRequest): string {
  const headers = Object.fromEntries(request.headers)
  const languages = new Negotiator({ headers }).languages()
  const defaultLocale = 'en'

  return match(languages, locales, defaultLocale)
}

export function middleware(request: NextRequest) {
  // Check if there is any supported locale in the pathname
  const { pathname } = request.nextUrl
  const pathnameHasLocale =
    locales.some((locale) => pathname.startsWith(`/${locale}`)) ||
    pathname.startsWith('/admin') ||
    pathname.startsWith('/api')

  if (pathnameHasLocale) return

  // Redirect if there is no locale
  const locale = getLocale(request)
  request.nextUrl.pathname = `/${locale}${pathname}`
  // e.g. incoming request is /products
  // The new URL is now /en-US/products
  return NextResponse.redirect(request.nextUrl)
}

export const config = {
  matcher: [
    // Skip all internal paths (_next)
    '/((?!_next).*)',
  ],
}
