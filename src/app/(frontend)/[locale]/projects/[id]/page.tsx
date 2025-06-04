import { getPayload } from 'payload'
import config from '@payload-config'
import { Project, Media } from '@/payload-types'
import RefreshRouterOnSave from '@/components/admin/RefreshRouteOnSave'
import { notFound } from 'next/navigation'
import Image from 'next/image'
import { getTranslations } from 'next-intl/server'
import { RichText } from '@payloadcms/richtext-lexical/react'

import { headers as getHeaders } from 'next/headers'
import { ReactNode } from 'react'

import '@styles/arrow.css'
import '@styles/descriptions.scss'
import { Link } from '@/i18n/navigation'

interface Props {
  params: Promise<{
    locale: 'en' | 'es'
    id: number
  }>
}

type ProjectImageSingle = Extract<NonNullable<Project['images']>[number], { blockType: 'image' }>
type ProjectImageGroup = Extract<
  NonNullable<Project['images']>[number],
  { blockType: 'imageGroup' }
>
type ProjectImage = Extract<NonNullable<Project['images']>[number], { blockType: 'image' }>

function DesktopImage(img: ProjectImage): ReactNode {
  const imageFile = img.image as Media
  const descPos = img.deskConf.descPos
  const descTopOrBottom = descPos === 'n' || descPos === 's'

  const flexDirection = descPos === 'w' ? 'row-reverse' : 'row'

  return (
    <figure
      className="relative flex justify-center items-center gap-x-12 size-fit"
      style={{ flexDirection }}
    >
      <Image
        src={imageFile.url!}
        alt={imageFile.alt}
        width={imageFile.width!}
        height={imageFile.height!}
        placeholder="blur"
        blurDataURL={imageFile.sizes!.loading!.url!}
        className="w-auto"
        style={{ height: `${img.deskConf.imageSize}svh` }}
      />
      {img.description && img.deskConf.descPos && (
        <figcaption
          className={`${descTopOrBottom ? 'max-w-9/10 absolute' : 'max-w-2/5'} ${descPos === 'n' ? 'bottom-21/20' : descPos === 's' ? 'top-21/20' : ''}`}
        >
          <RichText data={img.description} className="img-description" />
        </figcaption>
      )}
    </figure>
  )
}

function DesktopImageGroup(imgGroup: ProjectImageGroup): ReactNode {
  return (
    <div className="flex w-full min-h-svh py-25 justify-evenly">
      {imgGroup.images?.map((img) => (
        <div
          key={img.id}
          className={`${img.deskConf.groupAlign === 'top' ? 'self-start' : img.deskConf.groupAlign === 'bottom' ? 'self-end' : 'self-center'}`}
        >
          {DesktopImage(img as ProjectImageSingle)}
        </div>
      ))}
    </div>
  )
}

function PhoneImage(img: ProjectImage): ReactNode {
  const imageFile = img.image as Media
  if (!imageFile?.url) return 'No configurado'

  return (
    <figure
      key={imageFile.id}
      className={`${img.phoneConf?.imgAlign === 'overflow' ? '' : 'px-8'} py-25 gap-12 flex ${img.phoneConf.descPos === 'n' ? 'flex-col-reverse' : 'flex-col'}`}
      style={{ backgroundColor: img.bgColor }}
    >
      <Image
        src={imageFile.url!}
        alt={imageFile.alt}
        width={imageFile.width!}
        height={imageFile.height!}
        placeholder="blur"
        blurDataURL={imageFile.sizes!.loading!.url!}
        className={`max-h-160 ${
          img.phoneConf?.imgAlign === 'left'
            ? 'w-4/5 mr-auto'
            : img.phoneConf.imgAlign === 'right'
              ? 'w-4/5 ml-auto'
              : 'mx-auto'
        }`}
      />
      {img.description && img.phoneConf.descPos && (
        <figcaption className="max-w-9/10 mx-auto">
          <RichText data={img.description} className="img-description" />
        </figcaption>
      )}
    </figure>
  )
}

const Page = async ({ params }: Props) => {
  const payload = await getPayload({ config })
  const { locale, id } = await params
  const t = await getTranslations('Project')

  // Checking if the user is authenticated
  const headers = await getHeaders()
  const { user } = await payload.auth({ headers })

  const project: Project | null = await payload.findByID({
    collection: 'project',
    id,
    user,
    locale,
    depth: 2,
    draft: true, // Used for live preview. When an unauthenticated user access the site the published version will be returned
    overrideAccess: false,
    disableErrors: true, // Return null instead of throwing an error if the project doesn't exist
  })

  if (!project) notFound()

  const projects = await payload.find({
    collection: 'project',
    user,
    draft: true,
    overrideAccess: false,
  })

  const currentProjectIndex = projects.docs.findIndex((x) => x.id === project.id)
  const lastProject = currentProjectIndex === projects.totalDocs - 1

  return (
    <div className="relative">
      <div>
        <RefreshRouterOnSave />
        {project.images?.slice(0, 1).map((img) => {
          // This is assured to be a single image due to backend validation
          const image = img as ProjectImageSingle
          const imageFile = image.image as Media

          if (!imageFile) return 'Imagen no seleccionada.'

          return (
            <div key={img.id}>
              <div
                className="hidden lg:flex header-screen  items-center justify-evenly"
                style={{ backgroundColor: image.bgColor }}
                key={`${img.id}-desktop`}
              >
                <Image
                  src={imageFile.url!}
                  alt={imageFile.alt}
                  width={imageFile.width!}
                  height={imageFile.height!}
                  placeholder="blur"
                  blurDataURL={imageFile.sizes!.loading!.url!}
                  className="w-auto"
                  style={{ height: `${image.deskConf.imageSize}svh` }}
                />
                <figcaption className="max-w-2/5">
                  <div className="font-Nexa text-vector-cream flex w-full flex-col flex-wrap gap-y-20">
                    <p className="after:bg-vector-orange w-full text-right text-sm after:ml-2 after:mr-20 after:inline-block after:h-2 after:w-8">
                      {t('area')}: {project.area} m²
                    </p>
                    <h1 className="leading-none">{project.name}</h1>
                  </div>
                  <div className="my-5 h-fit shrink-0 grow">
                    <RichText
                      data={project.description}
                      className="img-description text-left font-Nexa size-full text-balance"
                    />
                  </div>
                </figcaption>
              </div>
              <div
                className="flex flex-col justify-evenly gap-y-20 py-20 lg:hidden"
                style={{ backgroundColor: image.bgColor }}
                key={`${img.id}-mobile`}
              >
                <Image
                  src={imageFile.url!}
                  alt={imageFile.alt}
                  width={imageFile.width!}
                  height={imageFile.height!}
                  placeholder="blur"
                  blurDataURL={imageFile.sizes!.loading!.url!}
                  className="max-w-3/4 mx-auto xl:max-w-full md:h-80 md:w-auto"
                />

                <div className="px-8">
                  <p className="after:bg-vector-orange w-full text-right text-sm after:ml-2 after:inline-block after:h-2 after:w-8 max-md:mb-10 md:after:mr-20">
                    {t('area')}: {project.area} m²
                  </p>
                  <h1 className="text-3xl! mb-6">{project.name}</h1>
                  <RichText data={project.description} className="img-description text-pretty" />
                </div>
              </div>
            </div>
          )
        })}
        <>
          <div className="hidden xl:block">
            {project.images?.slice(1).map((img) => (
              <div
                key={img.id}
                className="min-h-svh flex items-center justify-center"
                style={{
                  backgroundColor:
                    img.blockType === 'image'
                      ? img.bgColor
                      : img.blockType === 'imageGroup'
                        ? img.images?.at(-1)?.bgColor
                        : 'transparent',
                }}
              >
                {img.blockType === 'image' ? DesktopImage(img) : DesktopImageGroup(img)}
              </div>
            ))}
          </div>
          <div className="block xl:hidden">
            {project.images?.slice(1).map((img, i, arr) => (
              <div
                key={img.id}
                className={`${i === arr.length - 1 ? '[&>figure]:last:pb-50!' : ''}`}
              >
                {img.blockType === 'image'
                  ? PhoneImage(img)
                  : img.images?.map((groupedImg) => PhoneImage(groupedImg as ProjectImageSingle))}
              </div>
            ))}
          </div>
        </>
      </div>
      <Link
        href={lastProject ? '/conclusion' : `/projects?project=${currentProjectIndex + 1}`}
        className="absolute bottom-10 left-49/100 text-6xl font-bold"
        id="arrow"
      >
        &gt;
      </Link>
    </div>
  )
}

export default Page
