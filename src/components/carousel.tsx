'use client'
import '@styles/glide.css'

import Glide, { Controls, Swipe, Breakpoints } from '@glidejs/glide/dist/glide.modular.esm'
import '@glidejs/glide/dist/css/glide.core.min.css'
import { Media } from '@/payload-types'
import Image from 'next/image'
import { useEffect } from 'react'
import { Link } from '@/i18n/navigation'
import { useLocale } from 'next-intl'
import { useSearchParams } from 'next/navigation'
import { useTranslations } from 'next-intl'

interface Props {
  projects: { id: number; name: string; thumbnail?: number | Media | null | undefined }[]
}

export default function Carousel({ projects }: Props) {
  const searchParams = useSearchParams()

  // Get the index of the poject to show as the starting one
  // Using ! since undefined will translate to NaN and NaN || 0 = 0
  let projectIndex = parseInt(searchParams.get('project')!) || 0

  // Clamp the index to [0, projects.length]
  if (projectIndex > projects.length - 1 || projectIndex < 0) projectIndex = 0

  useEffect(() => {
    const carousel = new Glide('#carousel', {
      perView: 3,
      bound: true,
      startAt: projectIndex,
    }).mount({ Controls })

    const mobileCarousel = new Glide('#carousel-mobile', {
      perView: 2,
      type: 'carousel',
      startAt: projectIndex,
      breakpoints: {
        768: {
          perView: 1,
        },
      },
    }).mount({ Controls, Swipe, Breakpoints })

    // Destroying them here because when the route changes the glide instance doesn't get dsabled
    // and when navigating back it creates another one messing up the order. By destroying on route change it's ensured
    // that only one instance is ever active.
    return () => {
      carousel.destroy()
      mobileCarousel.destroy()
    }
  }, [projectIndex])

  const locale = useLocale()
  const t = useTranslations()

  return (
    <div className="bg-vector-grey flex flex-col justify-around set-header-screen">
      <h1 className="text-2xl! font-bold text-center">{t('NavBar.projects')}</h1>
      <div id="carousel" className="hidden lg:block">
        <div className="glide__track h-fit bg-vector-grey relative" data-glide-el="track">
          <ol className=" glide__slides h-fit! flex items-center justify-center">
            {projects.map(({ id, name, thumbnail }, i) => {
              thumbnail = thumbnail as Media

              if (!thumbnail?.url) return 'Imagen no configurada'

              return (
                <li className="glide__slide h-fit! flex justify-center items-center" key={id}>
                  <Link
                    href={`/projects/${id}`}
                    className="size-fit flex-col items-start transition-transform hover:cursor-pointer flex gap-y-5 pb-1"
                  >
                    <figure
                      className="h-100 relative overflow-hidden"
                      style={{ aspectRatio: '0.705', maxHeight: '50svh' }}
                    >
                      <Image
                        src={thumbnail.url!}
                        alt={thumbnail.alt!}
                        fill
                        sizes="33vw"
                        className="object-cover"
                      />
                      <div className="img-overlay"></div>
                      <figcaption className="font-Nexa uppercase text-center text-sm w-4/5 absolute z-20 top-1/2 left-1/2 bg-vector-black/70 -translate-1/2 border-1 border-vector-cream/30 p-2">
                        {i + 1}. {name}
                      </figcaption>
                    </figure>
                    <div className="text-vector-cream border-1 hover:scale-115 border-vector-cream transition-transform mx-auto py-2 px-5 rounded-lg">
                      {locale === 'es' ? 'Ver' : 'View'}
                    </div>
                  </Link>
                </li>
              )
            })}
          </ol>
          <div
            data-glide-el="controls"
            className="pointer-events-none flex items-center justify-end gap-x-5 px-20 text-4xl mt-5"
          >
            <button
              data-glide-dir="<"
              className="font-Nexa hover:scale-120 pointer-events-auto cursor-pointer transition-transform"
              aria-label={locale === 'es' ? 'Anterior' : 'Previous'}
            >
              <div className="font-Nexa gradient-background text-vector-cream h-fit font-extrabold">
                <div id="carouselArrow">&lt;</div>
              </div>
            </button>
            <button
              data-glide-dir=">"
              className="font-Nexa hover:scale-120 pointer-events-auto cursor-pointer transition-transform"
              aria-label={locale === 'es' ? 'Siguiente' : 'Next'}
            >
              <div className="font-Nexa gradient-background text-vector-cream h-fit font-extrabold">
                <div id="carouselArrow">&gt;</div>
              </div>
            </button>
          </div>
        </div>
      </div>
      <div
        id="carousel-mobile"
        className="lg:hidden flex flex-col gap-y-5 justify-center bg-vector-grey"
      >
        <div className="glide__track bg-vector-grey" data-glide-el="track">
          <ol className=" glide__slides">
            {projects.map(({ id, name, thumbnail }, i) => {
              thumbnail = thumbnail as Media

              if (!thumbnail?.url) return 'Sin miniatura seleccionada'

              return (
                <li className="glide__slide h-fit!" key={id}>
                  <Link
                    href={`/projects/${id}`}
                    className="mx-auto w-fit flex-col items-start transition-transform hover:cursor-pointer flex"
                  >
                    <figure
                      className="h-100 relative overflow-hidden"
                      style={{ aspectRatio: '0.705' }}
                    >
                      <Image
                        src={thumbnail.url!}
                        alt={thumbnail.alt!}
                        fill
                        sizes="80vw"
                        className="object-cover zoom"
                        placeholder="blur"
                        priority={i === projectIndex}
                        blurDataURL={thumbnail.sizes!.loading!.url!}
                        style={{
                          objectPosition: `${thumbnail.focalX}% ${thumbnail.focalY}%`,
                        }}
                      />
                      <div className="img-overlay"></div>
                      <figcaption className="font-Nexa uppercase font-bold text-center text-sm w-4/5 absolute z-20 top-1/2 left-1/2 bg-vector-black/40 -translate-1/2 border-1 border-vector-cream/30 p-2">
                        {i + 1}. {name}
                      </figcaption>
                    </figure>
                  </Link>
                </li>
              )
            })}
          </ol>
        </div>
        <div className="glide__bullets self-center" data-glide-el="controls[nav]">
          {projects.map((_, i) => (
            <button
              className="glide__bullet bg-vector-orange rounded-xl mx-2"
              data-glide-dir={`=${i}`}
              key={i}
            ></button>
          ))}
        </div>
      </div>
    </div>
  )
}
