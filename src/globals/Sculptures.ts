import { GlobalConfig } from 'payload'
import { colorField } from '@/lib/utils/colors'

export const Sculptures: GlobalConfig = {
  slug: 'sculpture',
  label: 'Esculturas',
  access: {
    read: ({ req }) => {
      // Only allowed authenticated users to access drafts
      if (req.user) return true

      return {
        or: [
          {
            _status: {
              equals: 'published',
            },
          },
          {
            _status: {
              exists: false,
            },
          },
        ],
      }
    },
  },
  admin: {
    description: 'Una imágen que contiene una escultura.',
    livePreview: {
      url: ({ locale }) => `${process.env.NEXT_PUBLIC_PAYLOAD_URL}/${locale}/sculptures`,
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
}
