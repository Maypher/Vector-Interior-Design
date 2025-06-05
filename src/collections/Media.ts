import type { CollectionConfig } from 'payload'

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
}
