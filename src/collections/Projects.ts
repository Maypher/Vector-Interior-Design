import type { CollectionConfig, Field } from 'payload'
import { Directions } from '@lib/selects'
import { Project } from '@/payload-types'
import { colorField } from '@/lib/utils/colors'
import { revalidatePath } from 'next/cache'
import { routing } from '@/i18n/routing'
import draftAccess from '@/lib/utils/access'
import purgeURL from '@/lib/utils/purge'
import { PAYLOAD_SECRET } from '@/lib/secrets'
import { ScrollingText } from '@/lib/payloadFields'

// Extracting it from imageConfig since there's an extra field for groups so I add it manually when setting the schema
const desktopConfig: Field = {
  name: 'deskConf',
  type: 'group',
  label: 'Configuración Escritorio',
  admin: {
    description:
      'La configuración que determina como se ve la imágen de un proyecto en escritorio.',
  },
  fields: [
    {
      name: 'imageSize',
      type: 'number',
      label: 'Tamaño de imagen',
      admin: {
        description: 'El tamaño de la imagen relativo al bloque que la contiene',
        step: 10,
        placeholder: '100%',
      },
      required: true,
      defaultValue: 100,
      min: 0,
      max: 100,
    },
    {
      type: 'select',
      name: 'descPos',
      label: 'Posición de Descripción',
      admin: {
        description: 'La posición de la descripción relativa a la imagen.',
        isClearable: true,
      },
      options: Directions,
    },
  ],
}

const imageConfig: Field[] = [
  {
    name: 'image',
    label: 'Imágen',
    type: 'upload',
    required: true,
    relationTo: 'media',
    admin: {
      description: 'Las imágenes de este proyecto.',
    },
  },
  {
    name: 'description',
    type: 'richText',
    label: 'Descripción',
    admin: {
      description: 'La descripción de la imagen',
    },
    required: false,
    localized: true,
  },
  colorField,
  {
    name: 'phoneConf',
    type: 'group',
    label: 'Configuración Teléfono',
    admin: {
      description:
        'La configuración que determina como la imagen de un proyecto se ve en dispositvos móbiles.',
    },
    fields: [
      {
        name: 'imgAlign',
        label: 'Alineación de Imagen',
        type: 'select',
        required: true,
        options: [
          {
            label: 'Izquierda',
            value: 'left',
          },
          {
            label: 'Derecha',
            value: 'right',
          },
          {
            label: 'Centrar',
            value: 'center',
          },
          {
            label: 'Sangrar',
            value: 'overflow',
          },
        ],
        defaultValue: 'center',
      },
      {
        type: 'row',
        fields: [
          {
            type: 'select',
            name: 'descPos',
            label: 'Posición de Descripción',
            admin: {
              description: 'La posición de la descripción relativa a la imagen.',
              isClearable: true,
            },
            options: Directions,
          },
        ],
      },
    ],
  },
]

export const Projects: CollectionConfig = {
  slug: 'project',
  labels: {
    singular: 'Proyecto',
    plural: 'Proyectos',
  },
  access: {
    read: draftAccess,
  },
  admin: {
    description: 'Sección principal de la página. Contiene todas las imagenes de una obra.',
    useAsTitle: 'name',
    preview: (doc, { locale }) => {
      const params = new URLSearchParams({
        path: `${locale}/projects/${doc.id}`,
        secret: PAYLOAD_SECRET,
      })

      return `/draft?${params.toString()}`
    },
  },
  orderable: true,
  fields: [
    {
      type: 'text',
      name: 'name',
      label: {
        es: 'Nombre',
      },
      admin: {
        description: 'El nombre del proyecto.',
      },
      localized: true,
      required: true,
    },
    {
      type: 'number',
      name: 'area',
      label: {
        es: 'Área',
      },
      required: true,
      admin: {
        description: 'El área del projecto en metros cuadrados.',
      },
    },
    {
      type: 'richText',
      name: 'description',
      label: {
        es: 'Descripción',
      },
      localized: true,
      admin: {
        description: 'Descripción general del projecto.',
      },
      required: true,
    },
    {
      name: 'images',
      label: 'Imágenes',
      type: 'blocks',
      minRows: 1,
      required: true,
      blocks: [
        {
          slug: 'image',
          labels: {
            singular: 'Imágen',
            plural: 'Imágenes',
          },
          fields: [...imageConfig, desktopConfig],
        },
        {
          slug: 'imageGroup',
          labels: {
            singular: 'Grupo de imágenes',
            plural: 'Grupos de imágenes',
          },
          fields: [
            {
              type: 'array',
              name: 'images',
              label: 'Imágenes',
              fields: [
                ...imageConfig,
                {
                  ...desktopConfig,
                  fields: [
                    ...desktopConfig.fields,
                    {
                      type: 'select',
                      name: 'groupAlign',
                      label: 'Alineación de grupo',
                      admin: {
                        description:
                          'Establece esta imagen como parte de un grupo y donde debería ser alineado en el contenedor del grupo.',
                        width: '50%',
                      },
                      options: [
                        {
                          label: 'Arriba',
                          value: 'top',
                        },
                        {
                          label: 'Medio',
                          value: 'middle',
                        },
                        {
                          label: 'Abajo',
                          value: 'bottom',
                        },
                      ],
                    },
                  ],
                } as Field,
              ],
            },
          ],
        },
        ScrollingText,
      ],
      validate: (imgs) => {
        const images = imgs as Project['images'] // Doing this because typing it in the function definition causes an error

        if (!images || images.length === 0) return 'Projecto debe tener al menos 1 imagen.'

        if (images?.at(0)?.blockType === 'imageGroup')
          return 'Primera imágen no puede ser un grupo.'
        return true
      },
    },
    {
      type: 'upload',
      name: 'thumbnail',
      label: 'Miniatura',
      required: true,
      admin: {
        description: 'La imágen que aparece en la lista de selección de proyectos.',
      },
      relationTo: 'media',
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
      async ({ doc }) => {
        // Ignore draft updates
        // Only revalidate cache when a document has been published
        if (doc._status === 'published') {
          const updateURL = `/projects/${doc.id}`

          // Revalidate all locales since when making changes not related
          // to localization it only updates that locale instead of all.
          // Revalidating everything (even if not needed) is an ease of use
          // tradeoff.
          routing.locales.forEach(async (locale) => {
            revalidatePath(`/${locale}${updateURL}`)
            await purgeURL(`${locale}${updateURL}`) // Purge nginx cache

            // Revalidate projects page in case name or thumbnail were changed
            revalidatePath(`/${locale}/projects`)
            await purgeURL(`${locale}/projects`)
          })
        }
      },
    ],
  },
}
