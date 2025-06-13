import { getPayload } from 'payload'
import config from '@payload-config'
import { draftMode } from 'next/headers'
import RefreshRouteOnSave from '@/components/admin/RefreshRouteOnSave'
import { MainPageImage, Media } from '@/payload-types'
import { RichText } from '@payloadcms/richtext-lexical/react'
import { getTranslations } from 'next-intl/server'
import headersConverter from '@/lib/utils/converter'

import ScrollToTopBtn from '@/components/mainPage/ScrollToTopBtn'
import Footer from '@/components/mainPage/Footer'
import NavLine from '@/components/mainPage/NavLine'

import React from 'react'
import { Link } from '@/i18n/navigation'

import '@styles/descriptions.scss'
import '@styles/nav.scss'
import ImageSkeleton from '@/components/global/ImageSkeleton'

type MainPageImageType = NonNullable<MainPageImage['images']>[number]

function imageBlock(
  image: Extract<NonNullable<MainPageImage['images']>[number], { blockType: 'image' }>,
) {
  // Flex direction for when description in left or right of image
  const descriptionPositionDesktop = image.deskConfig.descPos
  const descFlexDirectionDesktop =
    descriptionPositionDesktop === 'w'
      ? 'row-reverse'
      : descriptionPositionDesktop === 'e'
        ? 'row'
        : descriptionPositionDesktop === 'n'
          ? 'column-reverse'
          : 'column'

  // If the description is top or bottom then absolute position will be used
  // because using flex decenters the image
  const descTopOrBottomDesktop =
    descriptionPositionDesktop === 'n' || descriptionPositionDesktop === 's'

  const imgPosDesktop = image.deskConfig.imgPos
  const justifyPosDesktop = 'center'

  const imageFile = image.image as Media

  const descPosMobile = image.phoneConfig.descPos
  const flexDirectionMobile = descPosMobile === 's' ? 'column' : 'column-reverse'
  const overflowMobile = image.phoneConfig.overflow

  if (imageFile?.url)
    return (
      <>
        <div
          className="items-center relative hidden lg:flex desktop w-full"
          style={{
            backgroundColor: image.bgColor,
            justifyContent: justifyPosDesktop,
          }}
        >
          <figure
            key={image.id}
            style={{
              flexDirection: descFlexDirectionDesktop,
            }}
            className={`min-h-160 w-full items-center justify-center gap-x-15 xl:gap-x-15 flex gap-y-10 ${imgPosDesktop === 'left' ? 'mr-auto' : imgPosDesktop === 'right' ? 'ml-auto' : 'mx-auto'}`}
          >
            <div
              style={{ height: `${image.deskConfig.imgSize}svh` }}
              className="max-w-3/5 xl:max-w-11/20 2xl:max-w-full"
            >
              <ImageSkeleton
                image={image.image as Media}
                sizes={`(min-width: 1280px) 55vw, (min-width: 1440px) 70vw, 60vw`}
              />
            </div>
            {image.description && descriptionPositionDesktop && (
              <figcaption
                className={`${descTopOrBottomDesktop ? 'max-w-4/5 w-full' : 'max-w-2/5 w-fit'} text-pretty`}
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
        <figure
          className={`flex py-20 lg:hidden justify-center gap-y-16 size-full`}
          style={{
            flexDirection: flexDirectionMobile,
          }}
        >
          <ImageSkeleton
            image={imageFile}
            className={`shrink  ${overflowMobile ? '' : 'max-w-5/6 mx-auto'} max-h-140`}
            sizes={overflowMobile ? '100vw' : '90vw'}
          />
          {image.description && descPosMobile && (
            <figcaption className="max-w-5/6 mx-auto grow">
              <RichText
                data={image.description}
                converters={headersConverter}
                className="img-description"
              />
            </figcaption>
          )}
        </figure>
      </>
    )

  return <p>Sección no configurada</p>
}

function aboutUsBlock(message: Extract<MainPageImageType, { blockType: 'aboutUs' }>) {
  return (
    <section
      className="relative lg:h-svh w-full px-20 py-10 flex flex-col lg:flex-row items-center justify-center"
      id="aboutUs"
    >
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
      <div
        className="xl:h-[70svh] w-full flex flex-col xl:flex-row mt-20 lg:mt-0 gap-y-10 items-center justify-evenly overflow-hidden"
        id="nav"
      >
        <div
          style={{ height: `${image.imgSize}%` }}
          className="relative max-xl:h-fit! max-xl:w-full [&_img]:w-full!"
        >
          <ImageSkeleton image={image.image as Media} sizes={`(max-width: 1024px) 100vw, 50vw`} />
        </div>

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

export const dynamic = 'error'

export default async function MainPage({ params }: Props) {
  const payload = await getPayload({ config })
  const { locale } = await params
  const t = await getTranslations({ locale, namespace: 'NavBar' })

  const { isEnabled } = await draftMode()

  const mainPageImages: MainPageImage = await payload.findGlobal({
    slug: 'mainPageImages',
    depth: 5,
    draft: isEnabled,
    overrideAccess: isEnabled,
    locale,
  })

  return (
    <div className="grow flex flex-col justify-between">
      {isEnabled && <RefreshRouteOnSave />}
      <div className="grow flex flex-col justify-between">
        {!mainPageImages.images || mainPageImages.images.length === 0 ? (
          <div className="grow flex items-center justify-center">En configuración</div>
        ) : (
          mainPageImages.images?.slice(0, 1).map((image) => {
            return (
              <div
                id="welcome"
                className="header-screen flex justify-stretch items-center grow lg:px-10 mb-20 lg:mb-0"
                key={image.id}
                style={{ backgroundColor: image.bgColor }}
              >
                {image.blockType === 'image' && imageBlock(image)}
                <ul
                  className="w-fit mt-17 mb-auto text-[0.7rem] text-right [&_li]:w-fit hidden xl:flex flex-col gap-y-2 items-end ml-19"
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
          })
        )}
        {mainPageImages.images?.slice(1).map((image) => {
          return (
            <div
              style={{ backgroundColor: image.bgColor }}
              key={image.id}
              className="min-h-svh flex items-center lg:px-10"
            >
              {image.blockType === 'image' && imageBlock(image)}
              {image.blockType === 'aboutUs' && aboutUsBlock(image)}
              {image.blockType === 'navigation' && navBlock(image, t('projects'), t('sculptures'))}
            </div>
          )
        })}
      </div>
      <Footer />
    </div>
  )
}
