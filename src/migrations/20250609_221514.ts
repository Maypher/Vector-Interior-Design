import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

export async function up({ db, payload, req }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
   CREATE TYPE "public"."enum_conclusion_status" AS ENUM('draft', 'published');
  CREATE TYPE "public"."enum__conclusion_v_version_status" AS ENUM('draft', 'published');
  CREATE TYPE "public"."enum__conclusion_v_published_locale" AS ENUM('en', 'es');
  CREATE TABLE IF NOT EXISTS "conclusion" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"_status" "enum_conclusion_status" DEFAULT 'draft',
  	"updated_at" timestamp(3) with time zone,
  	"created_at" timestamp(3) with time zone
  );
  
  CREATE TABLE IF NOT EXISTS "conclusion_locales" (
  	"slogal" varchar,
  	"message" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "_conclusion_v" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"version__status" "enum__conclusion_v_version_status" DEFAULT 'draft',
  	"version_updated_at" timestamp(3) with time zone,
  	"version_created_at" timestamp(3) with time zone,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"snapshot" boolean,
  	"published_locale" "enum__conclusion_v_published_locale",
  	"latest" boolean,
  	"autosave" boolean
  );
  
  CREATE TABLE IF NOT EXISTS "_conclusion_v_locales" (
  	"version_slogal" varchar,
  	"version_message" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  DO $$ BEGIN
   ALTER TABLE "conclusion_locales" ADD CONSTRAINT "conclusion_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."conclusion"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_conclusion_v_locales" ADD CONSTRAINT "_conclusion_v_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_conclusion_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  CREATE INDEX IF NOT EXISTS "conclusion__status_idx" ON "conclusion" USING btree ("_status");
  CREATE UNIQUE INDEX IF NOT EXISTS "conclusion_locales_locale_parent_id_unique" ON "conclusion_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "_conclusion_v_version_version__status_idx" ON "_conclusion_v" USING btree ("version__status");
  CREATE INDEX IF NOT EXISTS "_conclusion_v_created_at_idx" ON "_conclusion_v" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "_conclusion_v_updated_at_idx" ON "_conclusion_v" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "_conclusion_v_snapshot_idx" ON "_conclusion_v" USING btree ("snapshot");
  CREATE INDEX IF NOT EXISTS "_conclusion_v_published_locale_idx" ON "_conclusion_v" USING btree ("published_locale");
  CREATE INDEX IF NOT EXISTS "_conclusion_v_latest_idx" ON "_conclusion_v" USING btree ("latest");
  CREATE INDEX IF NOT EXISTS "_conclusion_v_autosave_idx" ON "_conclusion_v" USING btree ("autosave");
  CREATE UNIQUE INDEX IF NOT EXISTS "_conclusion_v_locales_locale_parent_id_unique" ON "_conclusion_v_locales" USING btree ("_locale","_parent_id");`)
}

export async function down({ db, payload, req }: MigrateDownArgs): Promise<void> {
  await db.execute(sql`
   DROP TABLE "conclusion" CASCADE;
  DROP TABLE "conclusion_locales" CASCADE;
  DROP TABLE "_conclusion_v" CASCADE;
  DROP TABLE "_conclusion_v_locales" CASCADE;
  DROP TYPE "public"."enum_conclusion_status";
  DROP TYPE "public"."enum__conclusion_v_version_status";
  DROP TYPE "public"."enum__conclusion_v_published_locale";`)
}
