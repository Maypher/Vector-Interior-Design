import { GlobalConfig } from 'payload'
import { routing } from '@/i18n/routing'
import { revalidatePath } from 'next/cache'
import draftAccess from '@/lib/utils/access'
import purgeRoute from '@/lib/utils/purge'
import { PAYLOAD_SECRET } from '@/lib/secrets'

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
          path: `/${locale}/conclusion`,
          secret: PAYLOAD_SECRET,
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
      async ({ req, doc }) => {
        if (doc._status === 'published') {
          const updatedLocale = req.locale
          if (updatedLocale === 'all')
            routing.locales.map(async (locale) => {
              revalidatePath(`/${locale}/conclusion`)
              await purgeRoute(`${locale}/conclusion`)
            })
          else {
            revalidatePath(`/${updatedLocale}/conclusion`)
            await purgeRoute(`${updatedLocale}/conclusion`)
          }
        }
      },
    ],
  },
}
