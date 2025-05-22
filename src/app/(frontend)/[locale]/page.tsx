import { getPayload } from 'payload'
import config from '@payload-config'
import { headers } from 'next/headers'
import RefreshRouteOnSave from '@/components/admin/RefreshRouteOnSave'
import { MainPageImage, Media } from '@/payload-types'
import { RichText } from '@payloadcms/richtext-lexical/react'
import { getTranslations } from 'next-intl/server'

import ScrollToTopBtn from '@/components/mainPage/ScrollToTopBtn'
import Footer from '@/components/mainPage/Footer'
import NavLine from '@/components/mainPage/NavLine'
import SkeletonImage from '@/components/mainPage/skeletonImageMainPage'

import React from 'react'
import { Link } from '@/i18n/navigation'

import '@styles/descriptions.scss'
import '@styles/nav.scss'
import ImageSkeleton from '@/components/global/ImageSkeleton'

type MainPageImageType = NonNullable<MainPageImage['images']>[number]

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
          <ImageSkeleton image={image.image as Media} />
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
            {image.blockType === 'image' && <SkeletonImage image={image} />}
            <ul
              className="w-fit h-4/5 my-auto text-[0.7rem] text-right pr-10 [&_li]:w-fit hidden xl:flex flex-col gap-y-2 items-end"
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
            {image.blockType === 'image' && <SkeletonImage image={image} />}
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
