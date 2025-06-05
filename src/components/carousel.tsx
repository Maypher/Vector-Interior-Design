'use client'
import '@styles/glide.css'

import Glide, { Controls, Swipe } from '@glidejs/glide/dist/glide.modular.esm'
import '@glidejs/glide/dist/css/glide.core.min.css'
import { Media } from '@/payload-types'
import Image from 'next/image'
import { useEffect } from 'react'
import { Link } from '@/i18n/navigation'
import { useLocale } from 'next-intl'
import { useSearchParams } from 'next/navigation'

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
      perView: 1,
      type: 'carousel',
      startAt: projectIndex,
    }).mount({ Controls, Swipe })

    // Destroying them here because when the route changes the glide instance doesn't get dsabled
    // and when navigating back it creates another one messing up the order. By destroying on route change it's ensured
    // that only one instance is ever active.
    return () => {
      carousel.destroy()
      mobileCarousel.destroy()
    }
  }, [projectIndex])

  const locale = useLocale()

  return (
    <>
      <div id="carousel" className="hidden lg:block">
        <div
          className="glide__track bg-vector-grey header-screen relative flex flex-col pb-10"
          data-glide-el="track"
        >
          <ul className=" glide__slides grow flex items-center">
            {projects.map(({ id, name, thumbnail }) => {
              thumbnail = thumbnail as Media

              return (
                <li className="glide__slide flex items-center" key={id}>
                  <Link
                    href={`/projects/${id}`}
                    className="m-auto hidden w-fit flex-col items-start transition-transform hover:scale-110 hover:cursor-pointer lg:flex"
                  >
                    <figure>
                      <Image
                        src={thumbnail.url!}
                        alt={thumbnail.alt!}
                        width={thumbnail.width!}
                        height={thumbnail.height!}
                        sizes="33vw"
                        className="h-90 object-cover w-auto"
                      />
                      <figcaption>
                        <p
                          className="font-Nexa my-5 text-xs font-extralight"
                          style={{ letterSpacing: '0.1rem' }}
                        >
                          {name}
                        </p>
                      </figcaption>
                    </figure>
                  </Link>
                </li>
              )
            })}
          </ul>
          <div
            data-glide-el="controls"
            className="pointer-events-none flex items-center justify-end gap-x-5 px-20 text-xl"
          >
            <button
              data-glide-dir="<"
              className="font-Nexa hover:scale-120 pointer-events-auto cursor-pointer transition-transform"
              aria-label={locale === 'es' ? 'Anterior' : 'Previous'}
            >
              <div className="font-Nexa gradient-background text-vector-cream h-fit text-6xl font-extrabold">
                <div id="carouselArrow">&lt;</div>
              </div>
            </button>
            <button
              data-glide-dir=">"
              className="font-Nexa hover:scale-120 pointer-events-auto cursor-pointer transition-transform"
              aria-label={locale === 'es' ? 'Siguiente' : 'Next'}
            >
              <div className="font-Nexa gradient-background text-vector-cream h-fit text-6xl font-extrabold">
                <div id="carouselArrow">&gt;</div>
              </div>
            </button>
          </div>
        </div>
      </div>
      <div
        id="carousel-mobile"
        className="lg:hidden flex flex-col justify-center header-screen bg-vector-grey"
      >
        <div className="glide__track bg-vector-grey" data-glide-el="track">
          <ul className=" glide__slides">
            {projects.map(({ id, name, thumbnail }) => {
              thumbnail = thumbnail as Media

              return (
                <li className="glide__slide flex items-center" key={id}>
                  <Link
                    href={`/projects/${id}`}
                    className="m-auto w-fit flex-col items-start transition-transform hover:scale-110 hover:cursor-pointer flex"
                  >
                    <figure>
                      <Image
                        src={thumbnail.url!}
                        alt={thumbnail.alt!}
                        width={thumbnail.width!}
                        height={thumbnail.height!}
                        sizes="80vw"
                        className="h-90 object-cover w-auto"
                      />
                      <figcaption>
                        <p
                          className="font-Nexa my-5 text-xs font-extralight"
                          style={{ letterSpacing: '0.1rem' }}
                        >
                          {name}
                        </p>
                      </figcaption>
                    </figure>
                  </Link>
                </li>
              )
            })}
          </ul>
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
    </>
  )
}
