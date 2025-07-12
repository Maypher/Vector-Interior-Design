import { getPayload } from 'payload'
import config from '@payload-config'
import symbol from '@public/images/symbol.svg'
import whiteLogo from '@public/images/logoWhite.svg'
import { RichText } from '@payloadcms/richtext-lexical/react'
import { Link } from '@/i18n/navigation'
import Image from '@/components/global/Image'
import { draftMode } from 'next/headers'

export const dynamic = 'error'

export default async function Page({ params }: { params: Promise<{ locale: 'en' | 'es' }> }) {
  const payload = await getPayload({ config })
  const { isEnabled } = await draftMode()
  const { locale } = await params

  const conclusionData = await payload.findGlobal({
    slug: 'conclusion',
    overrideAccess: isEnabled,
    draft: isEnabled,
    locale: locale as 'es' | 'en',
  })

  return (
    <>
      <div className="set-header-screen bg-vector-grey min-h-150 relative flex items-center justify-evenly overflow-clip">
        <p
          className="text-vector-cream flex flex-col relative bottom-[12ch] text-xl font-thin italic leading-10 md:bottom-[4ch] md:text-4xl whitespace-pre"
          id="slogan"
        >
          {conclusionData.slogal}
        </p>

        <div className="-top-1/10 right-1/5 absolute flex h-full w-0.5 flex-col items-center overflow-visible md:relative md:right-auto md:ml-4 lg:ml-0">
          <Image src={symbol} alt="V" id="symbol" className="relative right-px min-w-52" />
          <div className="bg-vector-orange relative bottom-8 min-h-[200%] min-w-0.5"></div>
        </div>

        <div className="text-vector-cream bg-vector-grey relative z-20 hidden py-5 text-justify brightness-50 md:bg-transparent lg:block lg:basis-1/3 [&_strong]:text-white">
          <RichText data={conclusionData.message} />
        </div>
        <Link href="/" aria-label="home" className="transition-transform hover:scale-125">
          <Image
            src={whiteLogo}
            alt="Vector: Interior Design"
            className="hidden h-10 lg:block w-fit"
          />
        </Link>
        <div className="top-1/9 relative flex basis-1/2 max-w-[45svw] flex-col items-center gap-y-10 md:top-auto lg:hidden">
          <div className="bg-vector-grey">
            <div className="text-vector-cream text-justify brightness-50 lg:bg-transparent [&_strong]:text-white">
              <RichText data={conclusionData.message} />
            </div>
          </div>
          <Image
            src={whiteLogo}
            alt="Vector: Interior Design"
            className="h-10 self-center bg-vector-grey w-fit"
          />
          <div className="bg-vector-orange -bottom-15 absolute right-0 h-2 w-8"></div>
        </div>
        <div className="bg-vector-orange -bottom-15 right-10 hidden h-2 w-8 lg:absolute lg:block"></div>
      </div>
    </>
  )
}
