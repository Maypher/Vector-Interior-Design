import { getPayload } from 'payload'
import config from '@payload-config'
import { headers } from 'next/headers'
import RefreshRouteOnSave from '@/components/RefreshRouteOnSave'
import { MainPageImage, Media } from '@/payload-types'
import { RichText } from '@payloadcms/richtext-lexical/react'
import headersConverter from '@/lib/utils/converter'
import { getTranslations } from 'next-intl/server'

import ScrollToTopBtn from '@/components/mainPage/ScrollToTopBtn'
import Footer from '@/components/mainPage/Footer'
import NavLine from '@/components/mainPage/NavLine'

import React from 'react'
import Image from 'next/image'
import { Link } from '@/i18n/navigation'

import '@styles/descriptions.scss'
import '@styles/nav.scss'

type MainPageImageType = NonNullable<MainPageImage['images']>[number]

function imageBlock(image: Extract<MainPageImageType, { blockType: 'image' }>): React.ReactElement {
  const imageFile = image.image as Media

  // Flex direction for when description in left or right of image
  const descriptionPosition = image.deskConfig.descPos
  const descFlexDirection = descriptionPosition === 'w' ? 'row-reverse' : 'row'

  // If the description is top or bottom then absolute position will be used
  // because using flex decenters the image
  const descTopOrBottom = descriptionPosition === 'n' || descriptionPosition === 's'

  const imgPos = image.deskConfig.imgPos
  const justifyPos = imgPos === 'left' ? 'start' : imgPos == 'center' ? 'center' : 'end'
  if (imageFile && imageFile.url) {
    return (
      <div className="h-svh w-full flex items-center">
        <figure
          key={image.id}
          style={{
            backgroundColor: image.bgColor,
            flexDirection: descFlexDirection,
            justifyContent: justifyPos,
            paddingLeft: justifyPos === 'start' ? '5%' : '',
            paddingRight: justifyPos === 'end' ? '5%' : '',
            height: `${image.deskConfig.imgSize}%`,
          }}
          className={`grow w-fit flex items-center gap-x-20 ${descTopOrBottom ? 'relative' : ''}`}
        >
          <Image
            src={imageFile.url}
            alt={imageFile.alt}
            width={imageFile.width!}
            height={imageFile.height!}
            placeholder="blur"
            blurDataURL={imageFile.sizes!.loading!.url!}
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            className="h-full w-auto"
          />
          {image.description && image.deskConfig.descPos && (
            <figcaption
              className={`${descTopOrBottom ? 'absolute max-w-4/5' : 'max-w-2/5'} ${descriptionPosition === 's' ? 'top-21/20' : descriptionPosition === 'n' ? 'bottom-21/20' : ''}`}
            >
              <RichText
                data={image.description}
                className="img-description"
                converters={headersConverter}
              />
            </figcaption>
          )}
        </figure>
      </div>
    )
  }

  return <p>Sección no configurada</p>
}

function aboutUsBlock(message: Extract<MainPageImageType, { blockType: 'aboutUs' }>) {
  return (
    <section className="relative h-svh w-full px-20 flex items-center justify-center" id="aboutUs">
      <RichText data={message.description} className="about-us"></RichText>
      <ScrollToTopBtn />
    </section>
  )
}

function navBlock(
  image: Extract<MainPageImageType, { blockType: 'navigation' }>,
  projectsLabel: string,
  sculpturesLabel: string,
) {
  const imageFile = image.image as Media

  if (imageFile && imageFile.url) {
    return (
      <div className="h-[70svh] w-full flex items-center justify-evenly overflow-hidden" id="nav">
        <Image
          src={imageFile.url}
          alt={imageFile.alt}
          width={imageFile.width!}
          height={imageFile.height!}
          placeholder="blur"
          blurDataURL={imageFile.sizes!.loading!.url!}
          style={{ height: `${image.imgSize}%`, width: 'auto' }}
        />

        <ul className="flex items-center justify-center gap-5 p-5 text-xl lg:h-4/5">
          <li className="relative top-0 z-10 size-fit hover-link">
            <Link href="/sculptures">{sculpturesLabel}</Link>
          </li>
          <li aria-hidden={true}>
            <NavLine />
          </li>
          <li className="relative bottom-10 z-10 size-fit hover-link">
            <Link href="/projects">{projectsLabel}</Link>
          </li>
        </ul>
      </div>
    )
  }

  return <p>No configurado todavía</p>
}

interface Props {
  params: Promise<{
    locale: 'en' | 'es'
  }>
}

export default async function MainPage({ params }: Props) {
  const payload = await getPayload({ config })
  const { locale } = await params
  const reqHeaders = await headers()
  const t = await getTranslations('NavBar')

  const { user } = await payload.auth({ headers: reqHeaders })

  const mainPageImages: MainPageImage = await payload.findGlobal({
    slug: 'mainPageImages',
    depth: 5,
    draft: true,
    overrideAccess: false,
    user,
    locale,
  })

  return (
    <div>
      <RefreshRouteOnSave />
      {mainPageImages.images?.slice(0, 1).map((image) => {
        return (
          <div
            id="welcome"
            className="header-screen flex justify-stretch grow"
            key={image.id}
            style={{ backgroundColor: image.bgColor }}
          >
            {image.blockType === 'image' && imageBlock(image)}
            <ul
              className="w-fit h-4/5 my-auto text-[0.7rem] text-right pr-10 [&_li]:mb-2.5"
              style={{ letterSpacing: '0.05rem' }}
            >
              <li>
                <Link href="#aboutUs" className="hover-link">
                  {t('aboutUs')}
                </Link>
              </li>
              <li>
                <Link href="/projects" className="hover-link">
                  {t('projects')}
                </Link>
              </li>
              <li>
                <Link href="/sculptures" className="hover-link">
                  {t('sculptures')}
                </Link>
              </li>
              <li>
                <Link href="#contact" className="hover-link">
                  {t('contact')}
                </Link>
              </li>
            </ul>
          </div>
        )
      })}
      {mainPageImages.images?.slice(1).map((image) => {
        return (
          <div style={{ backgroundColor: image.bgColor }} key={image.id}>
            {image.blockType === 'image' && imageBlock(image)}
            {image.blockType === 'aboutUs' && aboutUsBlock(image)}
            {image.blockType === 'navigation' && navBlock(image, t('projects'), t('sculptures'))}
          </div>
        )
      })}
      <div className="relative flex items-center justify-center gap-x-5 py-20 bg-vector-black">
        <p className="border-vector-orange border-r-1 py-2 pr-5 text-2xl">Contacto</p>
        <a href="mailto:contact@vectorinterior.design" className="py-5">
          contact@vectorinterior.design
        </a>
      </div>
      <Footer />
    </div>
  )
}
