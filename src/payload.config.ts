// storage-adapter-import-placeholder
import { postgresAdapter } from '@payloadcms/db-postgres'
import { payloadCloudPlugin } from '@payloadcms/payload-cloud'
import { EMAIL_PASSWORD, PAYLOAD_SECRET } from './lib/secrets'
import { DATABASE_URI } from './lib/secrets'
import { nodemailerAdapter } from '@payloadcms/email-nodemailer'

import {
  lexicalEditor,
  FixedToolbarFeature,
  RelationshipFeature,
  UploadFeature,
} from '@payloadcms/richtext-lexical'
import path from 'path'
import { buildConfig } from 'payload'
import { fileURLToPath } from 'url'
import sharp from 'sharp'

import { Users } from '@collections/Users'
import { Media } from '@collections/Media'
import { Projects } from '@collections/Projects'
import { Sculptures } from './globals/Sculptures'
import { Conclusion } from './globals/Conclusion'
import MainPage from '@globals/MainPage'
import { migrations } from './migrations'

import { es } from 'payload/i18n/es'

const filename = fileURLToPath(import.meta.url)
const dirname = path.dirname(filename)

export default buildConfig({
  admin: {
    user: Users.slug,
    importMap: {
      baseDir: path.resolve(dirname),
    },
    livePreview: {
      url: process.env.NEXT_PUBLIC_PAYLOAD_URL,
      breakpoints: [
        {
          label: 'Móvil',
          name: 'mobile',
          width: 375,
          height: 667,
        },
        {
          label: 'Tablet',
          name: 'table',
          width: 600,
          height: 500,
        },
        {
          label: 'Escritorio',
          name: 'desktop',
          width: 1920,
          height: 1080,
        },
      ],
    },
    autoLogin:
      process.env.NODE_ENV !== 'production'
        ? {
            email: 'a@gmail.com',
            password: '1234',
            prefillOnly: true,
          }
        : false,
  },
  email: nodemailerAdapter({
    defaultFromAddress: 'contact@vectorinterior.design',
    defaultFromName: 'Vector: Interior Design',
    transportOptions: {
      host: process.env.SMTP_HOST,
      port: 465,
      secure: true,
      auth: {
        user: process.env.EMAIL_USER,
        pass: EMAIL_PASSWORD,
      },
    },
  }),
  localization: {
    locales: ['en', 'es'],
    defaultLocale: 'es',
  },
  i18n: {
    supportedLanguages: { es },
    fallbackLanguage: 'es',
  },
  collections: [Users, Media, Projects],
  globals: [MainPage, Sculptures, Conclusion],
  editor: lexicalEditor({
    features: ({ defaultFeatures }) => [
      ...defaultFeatures,
      FixedToolbarFeature({}),
      RelationshipFeature(),
      UploadFeature(),
    ],
  }),
  secret: PAYLOAD_SECRET,
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
  db: postgresAdapter({
    pool: {
      connectionString: DATABASE_URI,
    },
    prodMigrations: migrations,
  }),
  upload: {
    limits: {
      fileSize: 1e7,
    },
  },
  sharp,
  plugins: [
    payloadCloudPlugin(),
    // storage-adapter-placeholder
  ],
})
