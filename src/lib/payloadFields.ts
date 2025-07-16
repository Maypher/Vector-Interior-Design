import type { Block } from 'payload'
import { colorField } from './utils/colors'
import { Field } from 'payload'

export const ScrollingText: Block = {
  slug: 'animatedText',
  labels: {
    plural: 'texto animado',
    singular: 'texto animado',
  },
  fields: [
    {
      type: 'text',
      name: 'text',
      label: 'texto',
      localized: true,
      admin: {
        description: 'El texto a mostar moviendose a través de la pantalla',
      },
    },
    {
      ...colorField,
      name: 'textColor',
      label: 'color de Texto',
      admin: {
        description: 'El color del texto',
        components: {
          Field: '@/components/admin/ColorSelect.tsx',
        },
      },
    } as Field,
  ],
}
