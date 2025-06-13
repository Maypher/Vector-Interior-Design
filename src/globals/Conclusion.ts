import { GlobalConfig } from 'payload'
import { routing } from '@/i18n/routing'
import { revalidatePath } from 'next/cache'
import draftAccess from '@/lib/utils/access'

export const Conclusion: GlobalConfig = {
  slug: 'conclusion',
  label: 'Conclusión',
  access: {
    read: draftAccess,
  },
  admin: {
    description: 'Mesaje que aparece en la página de conclusión.',
    livePreview: {
      url: ({ locale }) => {
        const params = new URLSearchParams({
          path: `${locale}/conclusion`,
          secret: process.env.DRAFT_MODE_SECRET || '',
        })

        return `/draft?${params.toString()}`
      },
    },
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
  hooks: {
    afterChange: [
      ({ req, doc }) => {
        if (doc._status === 'published') {
          const updatedLocale = req.locale
          if (updatedLocale === 'all')
            routing.locales.map((locale) => revalidatePath(`/${locale}/conclusion`))
          else revalidatePath(`/${updatedLocale}/conclusion`)
        }
      },
    ],
  },
}
