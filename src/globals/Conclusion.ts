import { GlobalConfig } from 'payload'

export const Conclusion: GlobalConfig = {
  slug: 'conclusion',
  label: 'Conclusión',
  admin: {
    description: 'Mesaje que aparece en la página de conclusión.',
  },
  fields: [
    {
      type: 'textarea',
      name: 'slogal',
      label: 'Eslogan',
      admin: {
        description: 'El eslogan de la página.',
        rows: 3,
      },
      localized: true,
      required: true,
    },
    {
      type: 'richText',
      name: 'message',
      label: 'Mesaje',
      admin: {
        description: 'El mensaje explicativo del eslogan.',
      },
      localized: true,
      required: true,
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
