import type { CollectionConfig } from 'payload'
import { Directions, TextAlignment } from '@lib/selects'
import { Where } from 'payload'

export const Projects: CollectionConfig = {
  slug: 'project',
  labels: {
    singular: 'Proyecto',
    plural: 'Proyectos',
  },
  admin: {
    description: 'Sección principal de la página. Contiene todas las imagenes de una obra.',
    useAsTitle: 'name',
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
      admin: {
        description: 'Descripción general del projecto.',
      },
      required: true,
    },
    {
      name: 'images',
      type: 'array',
      minRows: 1,
      fields: [
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
          name: 'decription',
          type: 'richText',
          label: 'Descripción',
          admin: {
            description: 'La descripción de la imagen',
          },
          required: false,
          localized: true,
        },
        {
          name: 'deskConf',
          type: 'group',
          label: 'Configuración Escritorio',
          admin: {
            description:
              'La configuración que determina como se ve la imágen de un proyecto en escritorio.',
          },
          fields: [
            {
              type: 'row',
              fields: [
                {
                  type: 'select',
                  name: 'groupAlignment',
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
                {
                  name: 'groupEnd',
                  type: 'checkbox',
                  label: 'Forzar fin de grupo.',
                  admin: {
                    description:
                      'Forza un grupo a finalizar. Utilizado para lograr grupos consecutivos sin que se combinen.',
                  },
                },
              ],
            },
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
              type: 'row',
              fields: [
                {
                  type: 'select',
                  name: 'descriptionPosition',
                  label: 'Posición de Descripción',
                  admin: {
                    description: 'La posición de la descripción relativa a la imagen.',
                    isClearable: true,
                  },
                  options: Directions,
                },
                {
                  name: 'descriptionAlignment',
                  type: 'select',
                  label: 'Alineación de descripción',
                  admin: {
                    description: 'Alineación de la descripción.',
                    isClearable: true,
                  },
                  options: TextAlignment,
                  defaultValue: 'left',
                },
              ],
            },
          ],
        },
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
              name: 'imageAlignment',
              label: 'Alineación de Imagen',
              type: 'select',
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
                  name: 'descriptionPosition',
                  label: 'Posición de Descripción',
                  admin: {
                    description: 'La posición de la descripción relativa a la imagen.',
                    isClearable: true,
                  },
                  options: Directions,
                },
                {
                  type: 'select',
                  name: 'descriptionAlignment',
                  label: 'Alineación descripción',
                  admin: {
                    description: 'Alineación del texto de la descripción.',
                    isClearable: false,
                  },
                  options: TextAlignment,
                  defaultValue: 'left',
                  required: true,
                },
              ],
            },
          ],
        },
      ],
    },
    {
      type: 'relationship',
      name: 'thumbnail',
      label: 'Miniatura',
      admin: {
        description: 'La imágen que aparece en la lista de selección de proyectos.',
      },
      relationTo: 'media',
      filterOptions: ({ data }) => {
        const projectImages = data?.images?.map((image: any) => image?.image)?.filter(Boolean) || []

        const query: Where = {
          id: {
            in: projectImages,
          },
        }

        return query
      },
    },
  ],
  versions: {
    drafts: true,
  },
}
