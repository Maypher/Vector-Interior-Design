'use client'

import React from 'react'
import { RelationshipFieldClientComponent } from 'payload'
import { FieldLabel, FieldDescription } from '@payloadcms/ui'
import { useFormFields, useField, FieldType, usePayloadAPI } from '@payloadcms/ui'
import Image from 'next/image'
import { useState } from 'react'
import { Media } from '@/payload-types'

const ThumbnailSelect: RelationshipFieldClientComponent = ({ path, field }) => {
  const { value, setValue }: FieldType<string> = useField()

  const [page, setPage] = useState(1)
  const imagesPerPage = 4

  const imagesIds: number[] = useFormFields(([fields, _]) => {
    const ids: number[] = []

    // Doing this since the data is flattened and image data is in the key "images.[index].image"
    for (const key in fields) {
      const imageKey = key.match(/^images\.\d\.image/)?.at(0)

      if (imageKey) {
        ids.push(fields[imageKey].value as number)
      }
    }
    return ids
  })

  const [{ data, isLoading }] = usePayloadAPI(`/api/media?where[id][in]=${imagesIds}`)
  // the api query returns the images ordered by ID. This reorders it to be based on the actual order of images in the array
  const imagesToShow = imagesIds
    .map((id) => data.docs?.find((image: { id: number }) => image.id === id))
    .filter(Boolean)
  const imagesCount: number = data.docs?.length

  const pages = Math.ceil(data.docs?.length / imagesPerPage)

  return (
    <div>
      <FieldLabel
        path={path}
        required={field.required}
        label={field.label}
        localized={field.localized}
      />
      {!isLoading && imagesCount > 0 ? (
        <div>
          <div className="grid">
            {imagesToShow?.slice(page - 1, page + imagesPerPage - 1).map((image: Media) => (
              <button
                key={image.id}
                type="button"
                onClick={() => setValue(image.id)}
                className={`${parseInt(value) == image.id && 'selected'}`}
              >
                <Image
                  src={image.url!}
                  alt={image.alt}
                  width={image.width!}
                  height={image.height!}
                  key={image.id}
                  placeholder="blur"
                  blurDataURL={image.sizes!.loading!.url!}
                />
              </button>
            ))}
          </div>

          <div
            style={{
              display: 'flex',
              fontSize: '1.25rem',
              marginTop: '0.5rem',
              columnGap: '1.25rem',
            }}
          >
            <button
              style={{ display: page === 1 ? 'none' : 'block' }}
              type="button"
              onClick={() => setPage(Math.max(1, Math.min(page - 1, imagesCount)))}
            >
              &lt;
            </button>
            <p>
              {page}/{pages}
            </p>
            <button
              type="button"
              style={{ display: page === pages ? 'none' : 'block' }}
              onClick={() => setPage(Math.max(1, Math.min(page + 1, imagesCount)))}
            >
              &gt;
            </button>
          </div>
        </div>
      ) : imagesCount === 0 ? (
        'Proyecto no tiene imágenes.'
      ) : (
        'Cargando'
      )}
      <FieldDescription path={path} description={field.admin?.description} />
    </div>
  )
}

export default ThumbnailSelect
