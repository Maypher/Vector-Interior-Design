import { getPayload } from 'payload'
import config from '@payload-config'
import { headers } from 'next/headers'
import { Media, Sculpture } from '@/payload-types'
import Image from 'next/image'
import { RichText } from '@payloadcms/richtext-lexical/react'
import ScrollToTop from '@/components/sculptures/ScrollToTop'

import '@styles/descriptions.scss'
import { Fragment } from 'react'

function image(image: Media) {
  return (
    <Image
      src={image.url!}
      alt={image.alt}
      width={image.width!}
      height={image.height!}
      sizes="(max-width: 1024px) 90vw, 50vw"
      className="w-9/10 lg:w-auto lg:h-4/5 max-h-4/5 lg:max-h-none object-cover"
      placeholder="blur"
      blurDataURL={image.sizes!.loading!.url!}
      style={{ objectPosition: `${image.focalX!}% ${image.focalY!}%` }}
    />
  )
}

function singleSculpture(
  sculpture: Extract<NonNullable<Sculpture['sculptures']>[number], { blockType: 'sculpture' }>,
) {
  const imageFile = sculpture.image as Media
  return (
    <figure
      style={{ backgroundColor: sculpture.bgColor }}
      className="flex flex-col lg:flex-row items-center justify-evenly lg:justify-center size-full gap-x-20"
    >
      {image(imageFile)}
      {sculpture.description && (
        <figcaption>
          <RichText
            data={sculpture.description}
            className="text-[0.9rem] [&_em]:text-vector-orange"
          />
        </figcaption>
      )}
    </figure>
  )
}

function sculptureGroup(
  group: Extract<NonNullable<Sculpture['sculptures']>[number], { blockType: 'sculptureGroup' }>,
) {
  return (
    <figure
      className="lg:flex items-center justify-center w-full gap-20"
      style={{ backgroundColor: group.bgColor }}
    >
      {group.images?.map((sculpture, i) => {
        const imageFile = sculpture.image as Media
        const groupLength = group.images!.length
        const lastInGroup = i === groupLength - 1

        return (
          <Fragment key={sculpture.id}>
            <div className="lg:hidden w-full h-svh flex flex-col justify-evenly items-center">
              {image(imageFile)}
              {lastInGroup && group.description && (
                <figcaption>
                  <RichText
                    data={group.description}
                    className="text-[0.9rem] [&_em]:text-vector-orange"
                  />
                </figcaption>
              )}
            </div>
            <div
              className="hidden lg:block max-w-1/3"
              style={{ height: `calc(${groupLength - i * 0.4}/${groupLength} * 80%)` }}
            >
              {image(imageFile)}
            </div>
          </Fragment>
        )
      })}
      {group.description && (
        <figcaption className="hidden lg:block">
          <RichText data={group.description} className="text-[0.9rem] [&_em]:text-vector-orange" />
        </figcaption>
      )}
    </figure>
  )
}

export default async function Sculptures() {
  const payload = await getPayload({ config })
  const reqHeaders = await headers()

  const { user } = await payload.auth({ headers: reqHeaders })

  const sculptures = await payload.findGlobal({
    slug: 'sculpture',
    user,
    overrideAccess: true,
    draft: true,
  })

  return (
    <div>
      {sculptures.sculptures?.slice(0, 1).map((sculpture) => (
        <div className="set-header-screen flex items-stretch justify-stretch" key={sculpture.id}>
          {sculpture.blockType === 'sculpture'
            ? singleSculpture(sculpture)
            : sculptureGroup(sculpture)}
        </div>
      ))}
      {sculptures.sculptures?.slice(1).map((sculpture) => {
        const group = sculpture.blockType === 'sculptureGroup'

        return (
          <div
            className={`${group ? 'min-h-svh lg:h-svh' : 'h-svh'} flex items-stretch justify-stretch`}
            key={sculpture.id}
          >
            {group ? sculptureGroup(sculpture) : singleSculpture(sculpture)}
          </div>
        )
      })}
      <ScrollToTop backgroundColor={sculptures.sculptures!.at(-1)!.bgColor} />
    </div>
  )
}
