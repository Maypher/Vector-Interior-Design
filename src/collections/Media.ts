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
  upload: {
    mimeTypes: ['image/*'],
    imageSizes: [
      {
        name: 'loading',
        width: 10,
        withoutEnlargement: true,
      },
      {
        name: 'mobile',
        width: 800,
        withoutEnlargement: true,
      },
      {
        name: 'tablet',
        width: 1500,
        withoutEnlargement: true,
      },
      {
        name: 'desktop',
        width: 1920,
        withoutEnlargement: true,
      },
    ],
  },
}
