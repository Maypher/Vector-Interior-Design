'use client'

import { useState } from 'react'
import { MainPageImage, Media } from '@/payload-types'
import ImageSkeleton from '../global/ImageSkeleton'
import { RichText } from '@payloadcms/richtext-lexical/react'
import headersConverter from '@/lib/utils/converter'
import '@styles/skeleton.scss'

interface Props {
  image: Extract<NonNullable<MainPageImage['images']>[number], { blockType: 'image' }>
}

export default function SkeletonImage({ image }: Props) {
  // Flex direction for when description in left or right of image
  const descriptionPositionDesktop = image.deskConfig.descPos
  const descFlexDirectionDesktop = descriptionPositionDesktop === 'w' ? 'row-reverse' : 'row'

  // If the description is top or bottom then absolute position will be used
  // because using flex decenters the image
  const descTopOrBottomDesktop =
    descriptionPositionDesktop === 'n' || descriptionPositionDesktop === 's'

  const imgPosDesktop = image.deskConfig.imgPos
  const justifyPosDesktop =
    imgPosDesktop === 'left' ? 'start' : imgPosDesktop == 'center' ? 'center' : 'end'

  const imageFile = image.image as Media

  const descPosMobile = image.phoneConfig.descPos
  const flexDirectionMobile = descPosMobile === 's' ? 'column' : 'column-reverse'
  const overflowMobile = image.phoneConfig.overflow

  if (imageFile?.url)
    return (
      <>
        <div
          className="h-svh max-h-full items-center w-full relative hidden xl:flex desktop"
          style={{
            backgroundColor: image.bgColor,
            justifyContent: justifyPosDesktop,
            paddingLeft: justifyPosDesktop === 'start' ? '5%' : '',
            paddingRight: justifyPosDesktop === 'end' ? '5%' : '',
          }}
        >
          <figure
            key={image.id}
            style={{
              height: `${image.deskConfig.imgSize}%`,
              flexDirection: descFlexDirectionDesktop,
            }}
            className={`items-center gap-x-20 ${descTopOrBottomDesktop ? 'relative' : ''} flex`} // Using opacity-0 absolute because using hidden causes the image to not load
          >
            <div className="h-full shrink">
              <ImageSkeleton image={image.image as Media} />
            </div>
            {image.description && image.deskConfig.descPos && (
              <figcaption
                className={`${descTopOrBottomDesktop ? 'absolute max-w-4/5' : 'max-w-2/5 w-fit'} ${descriptionPositionDesktop === 's' ? 'top-21/20' : descriptionPositionDesktop === 'n' ? 'bottom-21/20' : ''}`}
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
          className={`flex py-20 xl:hidden justify-center gap-y-16 w-full h-auto [&_img]:w-full [&_img]:h-auto! ${overflowMobile ? 'px-17' : ''} mobile`}
          style={{
            flexDirection: flexDirectionMobile,
          }}
        >
          <ImageSkeleton image={imageFile} />
          {image.description && descPosMobile && (
            <figcaption className="max-w-5/6 mx-auto">
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
