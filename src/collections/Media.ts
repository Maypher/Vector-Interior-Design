import type { CollectionConfig } from 'payload'
import { getPayload } from 'payload'
import config from '@payload-config'
import { revalidatePath } from 'next/cache'
import purgeRoute from '@/lib/utils/purge'
import { routing } from '@/i18n/routing'

export const Media: CollectionConfig = {
  slug: 'media',
  labels: {
    singular: {
      es: 'Imágen',
    },
    plural: {
      es: 'Imágenes',
    },
  },
  access: {
    read: () => true,
  },
  fields: [
    {
      name: 'alt',
      type: 'text',
      required: true,
      localized: true,
      label: 'Imágen',
    },
  ],
  folders: true,
  upload: {
    mimeTypes: ['image/*'],
    imageSizes: [
      {
        name: 'loading',
        width: 10,
        withoutEnlargement: true,
      },
    ],
  },
  hooks: {
    afterChange: [
      async ({ req, data }) => {
        const payload = await getPayload({ config })

        // Determine if the image is a thumbnail of any project.
        // Done to update the projects page in case the focal point was changed.
        // Individual project update not really required since the image will always be shown
        // in its entirety.
        const isThumbnail = await payload.find({
          collection: 'project',
          where: {
            thumbnail: {
              equals: data.id,
            },
          },
          req,
          pagination: false,
        })

        if (isThumbnail.totalDocs > 0) {
          if (req.locale === 'all') {
            routing.locales.forEach((locale) => {
              revalidatePath(`/${locale}/projects`)
              purgeRoute(`${locale}/projects`)
            })
          } else {
            revalidatePath(`/${req.locale}/projects`)
            purgeRoute(`${req.locale}/projects`)
          }
        }
      },
    ],
  },
}
