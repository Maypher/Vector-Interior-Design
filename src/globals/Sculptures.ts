import { GlobalConfig } from 'payload'
import { colorField } from '@/lib/utils/colors'
import draftAccess from '@/lib/utils/access'
import { routing } from '@/i18n/routing'
import { revalidatePath } from 'next/cache'
import purgeRoute from '@/lib/utils/purge'

export const Sculptures: GlobalConfig = {
  slug: 'sculpture',
  label: 'Esculturas',
  access: {
    read: draftAccess,
  },
  admin: {
    description: 'Una imágen que contiene una escultura.',
    livePreview: {
      url: ({ locale }) => {
        const params = new URLSearchParams({
          path: `${locale}/sculptures`,
          secret: process.env.DRAFT_MODE_SECRET || '',
        })

        return `/draft?${params.toString()}`
      },
    },
  },
  fields: [
    {
      name: 'sculptures',
      label: 'Esculturas',
      type: 'blocks',
      blocks: [
        {
          slug: 'sculpture',
          labels: {
            plural: 'Esculturas',
            singular: 'Escultura',
          },
          fields: [
            {
              name: 'image',
              type: 'upload',
              relationTo: 'media',
              label: 'Imagen',
              required: true,
            },
            {
              name: 'description',
              type: 'richText',
              label: 'Descripción',
              localized: true,
              admin: {
                description:
                  'La descripción de la imagen. Colocar texto en itático para cambiar el color.',
              },
            },
            colorField,
          ],
        },
        {
          slug: 'sculptureGroup',
          labels: {
            singular: 'Grupo de esculturas',
            plural: 'Grupo de esculturas',
          },
          fields: [
            {
              name: 'images',
              type: 'array',
              fields: [
                {
                  type: 'upload',
                  name: 'image',
                  label: 'Imagen',
                  relationTo: 'media',
                },
              ],
            },
            {
              name: 'description',
              type: 'richText',
              label: 'Descripción',
              localized: true,
              admin: {
                description:
                  'La descripción del  grupo de imágenes. Colocar texto en itálico para cambiar el color.',
              },
            },
            colorField,
          ],
        },
      ],
    },
  ],
  versions: {
    drafts: {
      autosave: {
        interval: 1500,
        showSaveDraftButton: true,
      },
    },
  },
  hooks: {
    afterChange: [
      async ({ req, doc }) => {
        if (doc._status === 'published') {
          const updatedLocale = req.locale
          if (updatedLocale === 'all')
            routing.locales.map(async (locale) => {
              revalidatePath(`/${locale}/sculptures`)
              await purgeRoute(`${locale}/sculptures`)
            })
          else {
            revalidatePath(`/${updatedLocale}/sculptures`)
            await purgeRoute(`${updatedLocale}/sculptures`)
          }
        }
      },
    ],
  },
}
