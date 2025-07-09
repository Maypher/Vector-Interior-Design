import { TextFieldSingleValidation, Field } from 'payload'

export const validateHexColor: TextFieldSingleValidation = (value) => {
  return (
    value?.match(/^#(?:[0-9a-fA-F]{3}){1,2}$/)?.length === 1 || `${value} is not a valid hex color`
  )
}

export const colorField: Field = {
  name: 'bgColor',
  label: 'Color de fondo',
  type: 'text',
  validate: validateHexColor,
  hasMany: false,
  required: true,
  defaultValue: '#101214',
  admin: {
    description: 'El color del fondo de la imagen.',
    components: {
      Field: '@/components/admin/ColorSelect.tsx',
    },
  },
}
