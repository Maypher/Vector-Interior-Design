import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

export async function up({ db, payload, req }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
   CREATE TYPE "public"."enum_sculpture_status" AS ENUM('draft', 'published');
  CREATE TYPE "public"."enum__sculpture_v_version_status" AS ENUM('draft', 'published');
  CREATE TYPE "public"."enum__sculpture_v_published_locale" AS ENUM('en', 'es');
  CREATE TABLE IF NOT EXISTS "sculpture_blocks_sculpture" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"bg_color" varchar DEFAULT '#101214',
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "sculpture_blocks_sculpture_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" varchar NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "sculpture_blocks_sculpture_group_images" (
  	"_order" integer NOT NULL,
  	"_parent_id" varchar NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"image_id" integer
  );
  
  CREATE TABLE IF NOT EXISTS "sculpture_blocks_sculpture_group" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"bg_color" varchar DEFAULT '#101214',
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "sculpture_blocks_sculpture_group_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" varchar NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "sculpture" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"_status" "enum_sculpture_status" DEFAULT 'draft',
  	"updated_at" timestamp(3) with time zone,
  	"created_at" timestamp(3) with time zone
  );
  
  CREATE TABLE IF NOT EXISTS "_sculpture_v_blocks_sculpture" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"bg_color" varchar DEFAULT '#101214',
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_sculpture_v_blocks_sculpture_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_images" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"_uuid" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_sculpture_v_blocks_sculpture_group" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"bg_color" varchar DEFAULT '#101214',
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "_sculpture_v" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"version__status" "enum__sculpture_v_version_status" DEFAULT 'draft',
  	"version_updated_at" timestamp(3) with time zone,
  	"version_created_at" timestamp(3) with time zone,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"snapshot" boolean,
  	"published_locale" "enum__sculpture_v_published_locale",
  	"latest" boolean,
  	"autosave" boolean
  );
  
  DO $$ BEGIN
   ALTER TABLE "sculpture_blocks_sculpture" ADD CONSTRAINT "sculpture_blocks_sculpture_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "sculpture_blocks_sculpture" ADD CONSTRAINT "sculpture_blocks_sculpture_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."sculpture"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "sculpture_blocks_sculpture_locales" ADD CONSTRAINT "sculpture_blocks_sculpture_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."sculpture_blocks_sculpture"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "sculpture_blocks_sculpture_group_images" ADD CONSTRAINT "sculpture_blocks_sculpture_group_images_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "sculpture_blocks_sculpture_group_images" ADD CONSTRAINT "sculpture_blocks_sculpture_group_images_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."sculpture_blocks_sculpture_group"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "sculpture_blocks_sculpture_group" ADD CONSTRAINT "sculpture_blocks_sculpture_group_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."sculpture"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "sculpture_blocks_sculpture_group_locales" ADD CONSTRAINT "sculpture_blocks_sculpture_group_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."sculpture_blocks_sculpture_group"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_sculpture_v_blocks_sculpture" ADD CONSTRAINT "_sculpture_v_blocks_sculpture_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_sculpture_v_blocks_sculpture" ADD CONSTRAINT "_sculpture_v_blocks_sculpture_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_sculpture_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_sculpture_v_blocks_sculpture_locales" ADD CONSTRAINT "_sculpture_v_blocks_sculpture_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_sculpture_v_blocks_sculpture"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_sculpture_v_blocks_sculpture_group_images" ADD CONSTRAINT "_sculpture_v_blocks_sculpture_group_images_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_sculpture_v_blocks_sculpture_group_images" ADD CONSTRAINT "_sculpture_v_blocks_sculpture_group_images_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_sculpture_v_blocks_sculpture_group"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_sculpture_v_blocks_sculpture_group" ADD CONSTRAINT "_sculpture_v_blocks_sculpture_group_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_sculpture_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_sculpture_v_blocks_sculpture_group_locales" ADD CONSTRAINT "_sculpture_v_blocks_sculpture_group_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_sculpture_v_blocks_sculpture_group"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_order_idx" ON "sculpture_blocks_sculpture" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_parent_id_idx" ON "sculpture_blocks_sculpture" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_path_idx" ON "sculpture_blocks_sculpture" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_image_idx" ON "sculpture_blocks_sculpture" USING btree ("image_id");
  CREATE UNIQUE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_locales_locale_parent_id_unique" ON "sculpture_blocks_sculpture_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_group_images_order_idx" ON "sculpture_blocks_sculpture_group_images" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_group_images_parent_id_idx" ON "sculpture_blocks_sculpture_group_images" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_group_images_image_idx" ON "sculpture_blocks_sculpture_group_images" USING btree ("image_id");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_group_order_idx" ON "sculpture_blocks_sculpture_group" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_group_parent_id_idx" ON "sculpture_blocks_sculpture_group" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_group_path_idx" ON "sculpture_blocks_sculpture_group" USING btree ("_path");
  CREATE UNIQUE INDEX IF NOT EXISTS "sculpture_blocks_sculpture_group_locales_locale_parent_id_unique" ON "sculpture_blocks_sculpture_group_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "sculpture__status_idx" ON "sculpture" USING btree ("_status");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_order_idx" ON "_sculpture_v_blocks_sculpture" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_parent_id_idx" ON "_sculpture_v_blocks_sculpture" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_path_idx" ON "_sculpture_v_blocks_sculpture" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_image_idx" ON "_sculpture_v_blocks_sculpture" USING btree ("image_id");
  CREATE UNIQUE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_locales_locale_parent_id_unique" ON "_sculpture_v_blocks_sculpture_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_images_order_idx" ON "_sculpture_v_blocks_sculpture_group_images" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_images_parent_id_idx" ON "_sculpture_v_blocks_sculpture_group_images" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_images_image_idx" ON "_sculpture_v_blocks_sculpture_group_images" USING btree ("image_id");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_order_idx" ON "_sculpture_v_blocks_sculpture_group" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_parent_id_idx" ON "_sculpture_v_blocks_sculpture_group" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_path_idx" ON "_sculpture_v_blocks_sculpture_group" USING btree ("_path");
  CREATE UNIQUE INDEX IF NOT EXISTS "_sculpture_v_blocks_sculpture_group_locales_locale_parent_id_unique" ON "_sculpture_v_blocks_sculpture_group_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_version_version__status_idx" ON "_sculpture_v" USING btree ("version__status");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_created_at_idx" ON "_sculpture_v" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_updated_at_idx" ON "_sculpture_v" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_snapshot_idx" ON "_sculpture_v" USING btree ("snapshot");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_published_locale_idx" ON "_sculpture_v" USING btree ("published_locale");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_latest_idx" ON "_sculpture_v" USING btree ("latest");
  CREATE INDEX IF NOT EXISTS "_sculpture_v_autosave_idx" ON "_sculpture_v" USING btree ("autosave");`)
}

export async function down({ db, payload, req }: MigrateDownArgs): Promise<void> {
  await db.execute(sql`
   DROP TABLE "sculpture_blocks_sculpture" CASCADE;
  DROP TABLE "sculpture_blocks_sculpture_locales" CASCADE;
  DROP TABLE "sculpture_blocks_sculpture_group_images" CASCADE;
  DROP TABLE "sculpture_blocks_sculpture_group" CASCADE;
  DROP TABLE "sculpture_blocks_sculpture_group_locales" CASCADE;
  DROP TABLE "sculpture" CASCADE;
  DROP TABLE "_sculpture_v_blocks_sculpture" CASCADE;
  DROP TABLE "_sculpture_v_blocks_sculpture_locales" CASCADE;
  DROP TABLE "_sculpture_v_blocks_sculpture_group_images" CASCADE;
  DROP TABLE "_sculpture_v_blocks_sculpture_group" CASCADE;
  DROP TABLE "_sculpture_v_blocks_sculpture_group_locales" CASCADE;
  DROP TABLE "_sculpture_v" CASCADE;
  DROP TYPE "public"."enum_sculpture_status";
  DROP TYPE "public"."enum__sculpture_v_version_status";
  DROP TYPE "public"."enum__sculpture_v_published_locale";`)
}
