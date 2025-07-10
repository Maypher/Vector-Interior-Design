import { GlobalConfig } from 'payload'
import { Directions, ImagePositionMainPageDesktop } from '@/lib/selects'
import { colorField } from '@lib/utils/colors'
import { MainPageImage } from '@/payload-types'
import draftAccess from '@/lib/utils/access'
import { routing } from '@/i18n/routing'
import { revalidatePath } from 'next/cache'
import purgeRoute from '@/lib/utils/purge'

const MainPage: GlobalConfig = {
  slug: 'mainPageImages',
  label: 'Página principal',
  admin: {
    description: 'Configuración de todas las imágenes que aparecerán en la página principal.',
    livePreview: {
      url: ({ locale }) => {
        const params = new URLSearchParams({
          path: `${locale}/`,
          secret: process.env.DRAFT_MODE_SECRET || '',
        })

        return `/draft?${params.toString()}`
      },
    },
  },
  access: {
    read: draftAccess,
  },
  fields: [
    {
      name: 'images',
      label: {
        es: 'Imágenes',
      },
      admin: {
        description:
          'Imágenes que apareceran en la página principal. Pueden ser imágenes, sobre nosotros o navegación. Sobre nosotros y navegación son obligatorios y debe haber uno solo de cada uno.',
      },
      type: 'blocks',
      minRows: 2,
      validate: (value) => {
        const images = value as MainPageImage['images']

        if (!images) return 'Página principal debe tener imágenes.'

        // There must be only 1 of each
        let aboutUsCount = 0
        let navCount = 0

        for (const block of images) {
          if (block.blockType === 'aboutUs') aboutUsCount += 1
          else if (block.blockType === 'navigation') navCount += 1
        }

        if (aboutUsCount === 0) return 'Debe haber una sección "Nosotros".'
        else if (aboutUsCount > 1) return 'Solo puede haber una sección "Nosotros"'

        if (navCount === 0) return 'Debe haber una sección de navegación.'
        else if (navCount > 1) return 'Solo puede haber una sección de navegación.'

        return true
      },
      blocks: [
        {
          slug: 'image',
          labels: {
            plural: 'Imágenes',
            singular: 'Imagen',
          },
          fields: [
            {
              name: 'image',
              label: {
                es: 'Imágen',
              },
              admin: {
                description: 'La imágen que mostrar en la página principal.',
              },
              type: 'upload',
              relationTo: 'media',
              required: true,
            },
            {
              name: 'description',
              label: {
                es: 'Descripción',
              },
              admin: {
                description: 'La descripción de la imágen.',
              },
              type: 'richText',
              localized: true,
            },
            colorField,
            {
              name: 'phoneConfig',
              label: 'Configuración Móvil',
              type: 'group',
              admin: {
                description: 'Configuración de la imágen en dispositivos móviles.',
              },
              required: true,
              fields: [
                {
                  name: 'descPos',
                  label: 'Posición Descripción',
                  admin: {
                    description: 'Posición de la descripción relativa a la imagen.',
                  },
                  type: 'select',
                  options: Directions,
                },
                {
                  name: 'overflow',
                  label: 'Sangrar',
                  admin: {
                    description: 'Sangrar la imagen a los bordes de la pantalla.',
                  },
                  type: 'checkbox',
                },
              ],
            },
            {
              name: 'deskConfig',
              label: 'Configuración Escritorio',
              admin: {
                description: 'La configuración de como se verá una imágen en escritorios.',
              },
              type: 'group',
              required: true,
              fields: [
                {
                  name: 'imgPos',
                  label: 'Posición de imágen',
                  type: 'select',
                  options: ImagePositionMainPageDesktop,
                  admin: {
                    description: 'La posición de la imágen en su contenedor.',
                  },
                  defaultValue: 'center',
                  required: true,
                },
                {
                  name: 'imgSize',
                  label: 'Tamaño de imágen',
                  admin: {
                    description: 'El tamaño de la imagen relativo a su contenedor.',
                  },
                  type: 'number',
                  min: 0,
                  max: 100,
                  defaultValue: 100,
                  required: true,
                },
                {
                  name: 'descPos',
                  label: 'Posición de descripción',
                  admin: {
                    description: 'La posición de la descripción relativa a la imagen.',
                    isClearable: true,
                  },
                  type: 'select',
                  options: Directions,
                },
              ],
            },
          ],
        },
        {
          slug: 'aboutUs',
          imageURL: '/images/tony.jpg',
          imageAltText: 'Diseñador',
          labels: {
            singular: 'Sobre nostoros',
            plural: 'Sobre nosotros',
          },
          fields: [
            {
              name: 'description',
              label: 'Sobre nosotros',
              type: 'richText',
              admin: {
                description:
                  'El mensaje principal de "Sobre nosotros". La primera línea será más clara que el resto.',
              },
              localized: true,
              required: true,
            },
            colorField,
          ],
        },
        {
          slug: 'navigation',
          labels: {
            singular: 'Navegación',
            plural: 'Navegaciones',
          },
          fields: [
            {
              name: 'image',
              label: 'imágen',
              type: 'upload',
              relationTo: 'media',
            },
            {
              name: 'imgSize',
              label: 'Tamaño de imágen',
              type: 'number',
              min: 0,
              max: 100,
              required: true,
              defaultValue: 100,
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
              revalidatePath(`/${locale}`)
              await purgeRoute(`${locale}`)
            })
          else {
            revalidatePath(`/${updatedLocale}`)
            await purgeRoute(`${updatedLocale}`)
          }
        }
      },
    ],
  },
}

export default MainPage
