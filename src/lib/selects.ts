import type { OptionObject } from 'payload'

export const Directions: OptionObject[] = [
  { label: 'N', value: 'n' },
  { label: 'S', value: 's' },
  { label: 'E', value: 'e' },
  { label: 'O', value: 'w' },
]

export const TextAlignment: OptionObject[] = [
  { label: 'Izquierda', value: 'left' },
  { label: 'Justificar', value: 'justify' },
  { label: 'Centrar', value: 'center' },
  { label: 'Derecha', value: 'right' },
]

export const ImagePositionMainPageDesktop: OptionObject[] = [
  { label: 'Izquierda', value: 'left' },
  { label: 'Centro', value: 'center' },
  { label: 'Derecha', value: 'right' },
]

export const ImagePositionProjectPhone: OptionObject[] = [
  ...ImagePositionMainPageDesktop,
  { label: 'Sangrar', value: 'overflow' },
]
