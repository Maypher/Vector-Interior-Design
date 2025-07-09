import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

export async function up({ db, payload, req }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
   ALTER TABLE "project_locales" ADD COLUMN "description" jsonb;
  ALTER TABLE "_project_v_locales" ADD COLUMN "version_description" jsonb;
  ALTER TABLE "project" DROP COLUMN "description";
  ALTER TABLE "_project_v" DROP COLUMN "version_description";`)
}

export async function down({ db, payload, req }: MigrateDownArgs): Promise<void> {
  await db.execute(sql`
   ALTER TABLE "project" ADD COLUMN "description" jsonb;
  ALTER TABLE "_project_v" ADD COLUMN "version_description" jsonb;
  ALTER TABLE "project_locales" DROP COLUMN "description";
  ALTER TABLE "_project_v_locales" DROP COLUMN "version_description";`)
}
