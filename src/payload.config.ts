// storage-adapter-import-placeholder
import { sqliteAdapter } from '@payloadcms/db-sqlite'
import { payloadCloudPlugin } from '@payloadcms/payload-cloud'
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
import MainPage from '@globals/MainPage'

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
  },
  localization: {
    locales: ['en', 'es'],
    defaultLocale: 'es',
  },
  i18n: {
    supportedLanguages: { es },
    fallbackLanguage: 'es',
  },
  collections: [Users, Media, Projects],
  globals: [MainPage],
  editor: lexicalEditor({
    features: ({ defaultFeatures }) => [
      ...defaultFeatures,
      FixedToolbarFeature({}),
      RelationshipFeature(),
      UploadFeature(),
    ],
  }),
  secret: process.env.PAYLOAD_SECRET || '',
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
  db: sqliteAdapter({
    client: {
      url: process.env.DATABASE_URI || '',
    },
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
