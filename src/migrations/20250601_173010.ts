import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

export async function up({ db, payload, req }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
   CREATE TYPE "public"."_locales" AS ENUM('en', 'es');
  CREATE TYPE "public"."enum_project_blocks_image_phone_conf_img_align" AS ENUM('left', 'right', 'center', 'overflow');
  CREATE TYPE "public"."enum_project_blocks_image_phone_conf_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum_project_blocks_image_desk_conf_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum_project_blocks_image_group_images_phone_conf_img_align" AS ENUM('left', 'right', 'center', 'overflow');
  CREATE TYPE "public"."enum_project_blocks_image_group_images_phone_conf_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum_project_blocks_image_group_images_desk_conf_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum_project_blocks_image_group_images_desk_conf_group_align" AS ENUM('top', 'middle', 'bottom');
  CREATE TYPE "public"."enum_project_status" AS ENUM('draft', 'published');
  CREATE TYPE "public"."enum__project_v_blocks_image_phone_conf_img_align" AS ENUM('left', 'right', 'center', 'overflow');
  CREATE TYPE "public"."enum__project_v_blocks_image_phone_conf_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum__project_v_blocks_image_desk_conf_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum__project_v_blocks_image_group_images_phone_conf_img_align" AS ENUM('left', 'right', 'center', 'overflow');
  CREATE TYPE "public"."enum__project_v_blocks_image_group_images_phone_conf_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum__project_v_blocks_image_group_images_desk_conf_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum__project_v_blocks_image_group_images_desk_conf_group_align" AS ENUM('top', 'middle', 'bottom');
  CREATE TYPE "public"."enum__project_v_version_status" AS ENUM('draft', 'published');
  CREATE TYPE "public"."enum__project_v_published_locale" AS ENUM('en', 'es');
  CREATE TYPE "public"."enum_main_page_images_blocks_image_phone_config_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum_main_page_images_blocks_image_desk_config_img_pos" AS ENUM('left', 'center', 'right');
  CREATE TYPE "public"."enum_main_page_images_blocks_image_desk_config_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum_main_page_images_status" AS ENUM('draft', 'published');
  CREATE TYPE "public"."enum__main_page_images_v_blocks_image_phone_config_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum__main_page_images_v_blocks_image_desk_config_img_pos" AS ENUM('left', 'center', 'right');
  CREATE TYPE "public"."enum__main_page_images_v_blocks_image_desk_config_desc_pos" AS ENUM('n', 's', 'e', 'w');
  CREATE TYPE "public"."enum__main_page_images_v_version_status" AS ENUM('draft', 'published');
  CREATE TYPE "public"."enum__main_page_images_v_published_locale" AS ENUM('en', 'es');
  CREATE TABLE IF NOT EXISTS "users" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"email" varchar NOT NULL,
  	"reset_password_token" varchar,
  	"reset_password_expiration" timestamp(3) with time zone,
  	"salt" varchar,
  	"hash" varchar,
  	"login_attempts" numeric DEFAULT 0,
  	"lock_until" timestamp(3) with time zone
  );
  
  CREATE TABLE IF NOT EXISTS "media" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"folder_id" integer,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"url" varchar,
  	"thumbnail_u_r_l" varchar,
  	"filename" varchar,
  	"mime_type" varchar,
  	"filesize" numeric,
  	"width" numeric,
  	"height" numeric,
  	"focal_x" numeric,
  	"focal_y" numeric,
  	"sizes_loading_url" varchar,
  	"sizes_loading_width" numeric,
  	"sizes_loading_height" numeric,
  	"sizes_loading_mime_type" varchar,
  	"sizes_loading_filesize" numeric,
  	"sizes_loading_filename" varchar,
  	"sizes_mobile_url" varchar,
  	"sizes_mobile_width" numeric,
  	"sizes_mobile_height" numeric,
  	"sizes_mobile_mime_type" varchar,
  	"sizes_mobile_filesize" numeric,
  	"sizes_mobile_filename" varchar,
  	"sizes_tablet_url" varchar,
  	"sizes_tablet_width" numeric,
  	"sizes_tablet_height" numeric,
  	"sizes_tablet_mime_type" varchar,
  	"sizes_tablet_filesize" numeric,
  	"sizes_tablet_filename" varchar,
  	"sizes_desktop_url" varchar,
  	"sizes_desktop_width" numeric,
  	"sizes_desktop_height" numeric,
  	"sizes_desktop_mime_type" varchar,
  	"sizes_desktop_filesize" numeric,
  	"sizes_desktop_filename" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "media_locales" (
  	"alt" varchar NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "project_blocks_image" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"bg_color" varchar DEFAULT '#101214',
  	"phone_conf_img_align" "enum_project_blocks_image_phone_conf_img_align" DEFAULT 'center',
  	"phone_conf_desc_pos" "enum_project_blocks_image_phone_conf_desc_pos",
  	"desk_conf_image_size" numeric DEFAULT 100,
  	"desk_conf_desc_pos" "enum_project_blocks_image_desk_conf_desc_pos",
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "project_blocks_image_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" varchar NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "project_blocks_image_group_images" (
  	"_order" integer NOT NULL,
  	"_parent_id" varchar NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"bg_color" varchar DEFAULT '#101214',
  	"phone_conf_img_align" "enum_project_blocks_image_group_images_phone_conf_img_align" DEFAULT 'center',
  	"phone_conf_desc_pos" "enum_project_blocks_image_group_images_phone_conf_desc_pos",
  	"desk_conf_image_size" numeric DEFAULT 100,
  	"desk_conf_desc_pos" "enum_project_blocks_image_group_images_desk_conf_desc_pos",
  	"desk_conf_group_align" "enum_project_blocks_image_group_images_desk_conf_group_align"
  );
  
  CREATE TABLE IF NOT EXISTS "project_blocks_image_group_images_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" varchar NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "project_blocks_image_group" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "project" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"_order" varchar,
  	"area" numeric,
  	"description" jsonb,
  	"thumbnail_id" integer,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"_status" "enum_project_status" DEFAULT 'draft'
  );
  
  CREATE TABLE IF NOT EXISTS "project_locales" (
  	"name" varchar,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "_project_v_blocks_image" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"bg_color" varchar DEFAULT '#101214',
  	"phone_conf_img_align" "enum__project_v_blocks_image_phone_conf_img_align" DEFAULT 'center',
  	"phone_conf_desc_pos" "enum__project_v_blocks_image_phone_conf_desc_pos",
  	"desk_conf_image_size" numeric DEFAULT 100,
  	"desk_conf_desc_pos" "enum__project_v_blocks_image_desk_conf_desc_pos",
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_project_v_blocks_image_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "_project_v_blocks_image_group_images" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"bg_color" varchar DEFAULT '#101214',
  	"phone_conf_img_align" "enum__project_v_blocks_image_group_images_phone_conf_img_align" DEFAULT 'center',
  	"phone_conf_desc_pos" "enum__project_v_blocks_image_group_images_phone_conf_desc_pos",
  	"desk_conf_image_size" numeric DEFAULT 100,
  	"desk_conf_desc_pos" "enum__project_v_blocks_image_group_images_desk_conf_desc_pos",
  	"desk_conf_group_align" "enum__project_v_blocks_image_group_images_desk_conf_group_align",
  	"_uuid" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_project_v_blocks_image_group_images_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "_project_v_blocks_image_group" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_project_v" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"parent_id" integer,
  	"version__order" varchar,
  	"version_area" numeric,
  	"version_description" jsonb,
  	"version_thumbnail_id" integer,
  	"version_updated_at" timestamp(3) with time zone,
  	"version_created_at" timestamp(3) with time zone,
  	"version__status" "enum__project_v_version_status" DEFAULT 'draft',
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"snapshot" boolean,
  	"published_locale" "enum__project_v_published_locale",
  	"latest" boolean,
  	"autosave" boolean
  );
  
  CREATE TABLE IF NOT EXISTS "_project_v_locales" (
  	"version_name" varchar,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "payload_folders" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"name" varchar NOT NULL,
  	"folder_id" integer,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "payload_locked_documents" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"global_slug" varchar,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "payload_locked_documents_rels" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"order" integer,
  	"parent_id" integer NOT NULL,
  	"path" varchar NOT NULL,
  	"users_id" integer,
  	"media_id" integer,
  	"project_id" integer,
  	"payload_folders_id" integer
  );
  
  CREATE TABLE IF NOT EXISTS "payload_preferences" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"key" varchar,
  	"value" jsonb,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "payload_preferences_rels" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"order" integer,
  	"parent_id" integer NOT NULL,
  	"path" varchar NOT NULL,
  	"users_id" integer
  );
  
  CREATE TABLE IF NOT EXISTS "payload_migrations" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"name" varchar,
  	"batch" numeric,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "main_page_images_blocks_image" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"bg_color" varchar DEFAULT '#101214',
  	"phone_config_desc_pos" "enum_main_page_images_blocks_image_phone_config_desc_pos",
  	"phone_config_overflow" boolean,
  	"desk_config_img_pos" "enum_main_page_images_blocks_image_desk_config_img_pos" DEFAULT 'center',
  	"desk_config_img_size" numeric DEFAULT 100,
  	"desk_config_desc_pos" "enum_main_page_images_blocks_image_desk_config_desc_pos",
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "main_page_images_blocks_image_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" varchar NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "main_page_images_blocks_about_us" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"bg_color" varchar DEFAULT '#101214',
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "main_page_images_blocks_about_us_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" varchar NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "main_page_images_blocks_navigation" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"img_size" numeric DEFAULT 100,
  	"bg_color" varchar DEFAULT '#101214',
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "main_page_images" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"_status" "enum_main_page_images_status" DEFAULT 'draft',
  	"updated_at" timestamp(3) with time zone,
  	"created_at" timestamp(3) with time zone
  );
  
  CREATE TABLE IF NOT EXISTS "_main_page_images_v_blocks_image" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"bg_color" varchar DEFAULT '#101214',
  	"phone_config_desc_pos" "enum__main_page_images_v_blocks_image_phone_config_desc_pos",
  	"phone_config_overflow" boolean,
  	"desk_config_img_pos" "enum__main_page_images_v_blocks_image_desk_config_img_pos" DEFAULT 'center',
  	"desk_config_img_size" numeric DEFAULT 100,
  	"desk_config_desc_pos" "enum__main_page_images_v_blocks_image_desk_config_desc_pos",
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_main_page_images_v_blocks_image_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "_main_page_images_v_blocks_about_us" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"bg_color" varchar DEFAULT '#101214',
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_main_page_images_v_blocks_about_us_locales" (
  	"description" jsonb,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE IF NOT EXISTS "_main_page_images_v_blocks_navigation" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"image_id" integer,
  	"img_size" numeric DEFAULT 100,
  	"bg_color" varchar DEFAULT '#101214',
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE IF NOT EXISTS "_main_page_images_v" (
  	"id" serial PRIMARY KEY NOT NULL,
  	"version__status" "enum__main_page_images_v_version_status" DEFAULT 'draft',
  	"version_updated_at" timestamp(3) with time zone,
  	"version_created_at" timestamp(3) with time zone,
  	"created_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"updated_at" timestamp(3) with time zone DEFAULT now() NOT NULL,
  	"snapshot" boolean,
  	"published_locale" "enum__main_page_images_v_published_locale",
  	"latest" boolean,
  	"autosave" boolean
  );
  
  DO $$ BEGIN
   ALTER TABLE "media" ADD CONSTRAINT "media_folder_id_payload_folders_id_fk" FOREIGN KEY ("folder_id") REFERENCES "public"."payload_folders"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "media_locales" ADD CONSTRAINT "media_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."media"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project_blocks_image" ADD CONSTRAINT "project_blocks_image_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project_blocks_image" ADD CONSTRAINT "project_blocks_image_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."project"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project_blocks_image_locales" ADD CONSTRAINT "project_blocks_image_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."project_blocks_image"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project_blocks_image_group_images" ADD CONSTRAINT "project_blocks_image_group_images_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project_blocks_image_group_images" ADD CONSTRAINT "project_blocks_image_group_images_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."project_blocks_image_group"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project_blocks_image_group_images_locales" ADD CONSTRAINT "project_blocks_image_group_images_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."project_blocks_image_group_images"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project_blocks_image_group" ADD CONSTRAINT "project_blocks_image_group_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."project"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project" ADD CONSTRAINT "project_thumbnail_id_media_id_fk" FOREIGN KEY ("thumbnail_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "project_locales" ADD CONSTRAINT "project_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."project"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v_blocks_image" ADD CONSTRAINT "_project_v_blocks_image_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v_blocks_image" ADD CONSTRAINT "_project_v_blocks_image_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_project_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v_blocks_image_locales" ADD CONSTRAINT "_project_v_blocks_image_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_project_v_blocks_image"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v_blocks_image_group_images" ADD CONSTRAINT "_project_v_blocks_image_group_images_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v_blocks_image_group_images" ADD CONSTRAINT "_project_v_blocks_image_group_images_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_project_v_blocks_image_group"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v_blocks_image_group_images_locales" ADD CONSTRAINT "_project_v_blocks_image_group_images_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_project_v_blocks_image_group_images"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v_blocks_image_group" ADD CONSTRAINT "_project_v_blocks_image_group_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_project_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v" ADD CONSTRAINT "_project_v_parent_id_project_id_fk" FOREIGN KEY ("parent_id") REFERENCES "public"."project"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v" ADD CONSTRAINT "_project_v_version_thumbnail_id_media_id_fk" FOREIGN KEY ("version_thumbnail_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_project_v_locales" ADD CONSTRAINT "_project_v_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_project_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "payload_folders" ADD CONSTRAINT "payload_folders_folder_id_payload_folders_id_fk" FOREIGN KEY ("folder_id") REFERENCES "public"."payload_folders"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "payload_locked_documents_rels" ADD CONSTRAINT "payload_locked_documents_rels_parent_fk" FOREIGN KEY ("parent_id") REFERENCES "public"."payload_locked_documents"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "payload_locked_documents_rels" ADD CONSTRAINT "payload_locked_documents_rels_users_fk" FOREIGN KEY ("users_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "payload_locked_documents_rels" ADD CONSTRAINT "payload_locked_documents_rels_media_fk" FOREIGN KEY ("media_id") REFERENCES "public"."media"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "payload_locked_documents_rels" ADD CONSTRAINT "payload_locked_documents_rels_project_fk" FOREIGN KEY ("project_id") REFERENCES "public"."project"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "payload_locked_documents_rels" ADD CONSTRAINT "payload_locked_documents_rels_payload_folders_fk" FOREIGN KEY ("payload_folders_id") REFERENCES "public"."payload_folders"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "payload_preferences_rels" ADD CONSTRAINT "payload_preferences_rels_parent_fk" FOREIGN KEY ("parent_id") REFERENCES "public"."payload_preferences"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "payload_preferences_rels" ADD CONSTRAINT "payload_preferences_rels_users_fk" FOREIGN KEY ("users_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "main_page_images_blocks_image" ADD CONSTRAINT "main_page_images_blocks_image_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "main_page_images_blocks_image" ADD CONSTRAINT "main_page_images_blocks_image_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."main_page_images"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "main_page_images_blocks_image_locales" ADD CONSTRAINT "main_page_images_blocks_image_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."main_page_images_blocks_image"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "main_page_images_blocks_about_us" ADD CONSTRAINT "main_page_images_blocks_about_us_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."main_page_images"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "main_page_images_blocks_about_us_locales" ADD CONSTRAINT "main_page_images_blocks_about_us_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."main_page_images_blocks_about_us"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "main_page_images_blocks_navigation" ADD CONSTRAINT "main_page_images_blocks_navigation_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "main_page_images_blocks_navigation" ADD CONSTRAINT "main_page_images_blocks_navigation_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."main_page_images"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_main_page_images_v_blocks_image" ADD CONSTRAINT "_main_page_images_v_blocks_image_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_main_page_images_v_blocks_image" ADD CONSTRAINT "_main_page_images_v_blocks_image_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_main_page_images_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_main_page_images_v_blocks_image_locales" ADD CONSTRAINT "_main_page_images_v_blocks_image_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_main_page_images_v_blocks_image"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_main_page_images_v_blocks_about_us" ADD CONSTRAINT "_main_page_images_v_blocks_about_us_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_main_page_images_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_main_page_images_v_blocks_about_us_locales" ADD CONSTRAINT "_main_page_images_v_blocks_about_us_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_main_page_images_v_blocks_about_us"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_main_page_images_v_blocks_navigation" ADD CONSTRAINT "_main_page_images_v_blocks_navigation_image_id_media_id_fk" FOREIGN KEY ("image_id") REFERENCES "public"."media"("id") ON DELETE set null ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  DO $$ BEGIN
   ALTER TABLE "_main_page_images_v_blocks_navigation" ADD CONSTRAINT "_main_page_images_v_blocks_navigation_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_main_page_images_v"("id") ON DELETE cascade ON UPDATE no action;
  EXCEPTION
   WHEN duplicate_object THEN null;
  END $$;
  
  CREATE INDEX IF NOT EXISTS "users_updated_at_idx" ON "users" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "users_created_at_idx" ON "users" USING btree ("created_at");
  CREATE UNIQUE INDEX IF NOT EXISTS "users_email_idx" ON "users" USING btree ("email");
  CREATE INDEX IF NOT EXISTS "media_folder_idx" ON "media" USING btree ("folder_id");
  CREATE INDEX IF NOT EXISTS "media_updated_at_idx" ON "media" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "media_created_at_idx" ON "media" USING btree ("created_at");
  CREATE UNIQUE INDEX IF NOT EXISTS "media_filename_idx" ON "media" USING btree ("filename");
  CREATE INDEX IF NOT EXISTS "media_sizes_loading_sizes_loading_filename_idx" ON "media" USING btree ("sizes_loading_filename");
  CREATE INDEX IF NOT EXISTS "media_sizes_mobile_sizes_mobile_filename_idx" ON "media" USING btree ("sizes_mobile_filename");
  CREATE INDEX IF NOT EXISTS "media_sizes_tablet_sizes_tablet_filename_idx" ON "media" USING btree ("sizes_tablet_filename");
  CREATE INDEX IF NOT EXISTS "media_sizes_desktop_sizes_desktop_filename_idx" ON "media" USING btree ("sizes_desktop_filename");
  CREATE UNIQUE INDEX IF NOT EXISTS "media_locales_locale_parent_id_unique" ON "media_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_order_idx" ON "project_blocks_image" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_parent_id_idx" ON "project_blocks_image" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_path_idx" ON "project_blocks_image" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_image_idx" ON "project_blocks_image" USING btree ("image_id");
  CREATE UNIQUE INDEX IF NOT EXISTS "project_blocks_image_locales_locale_parent_id_unique" ON "project_blocks_image_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_group_images_order_idx" ON "project_blocks_image_group_images" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_group_images_parent_id_idx" ON "project_blocks_image_group_images" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_group_images_image_idx" ON "project_blocks_image_group_images" USING btree ("image_id");
  CREATE UNIQUE INDEX IF NOT EXISTS "project_blocks_image_group_images_locales_locale_parent_id_unique" ON "project_blocks_image_group_images_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_group_order_idx" ON "project_blocks_image_group" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_group_parent_id_idx" ON "project_blocks_image_group" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "project_blocks_image_group_path_idx" ON "project_blocks_image_group" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "project__order_idx" ON "project" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "project_thumbnail_idx" ON "project" USING btree ("thumbnail_id");
  CREATE INDEX IF NOT EXISTS "project_updated_at_idx" ON "project" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "project_created_at_idx" ON "project" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "project__status_idx" ON "project" USING btree ("_status");
  CREATE UNIQUE INDEX IF NOT EXISTS "project_locales_locale_parent_id_unique" ON "project_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_order_idx" ON "_project_v_blocks_image" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_parent_id_idx" ON "_project_v_blocks_image" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_path_idx" ON "_project_v_blocks_image" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_image_idx" ON "_project_v_blocks_image" USING btree ("image_id");
  CREATE UNIQUE INDEX IF NOT EXISTS "_project_v_blocks_image_locales_locale_parent_id_unique" ON "_project_v_blocks_image_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_group_images_order_idx" ON "_project_v_blocks_image_group_images" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_group_images_parent_id_idx" ON "_project_v_blocks_image_group_images" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_group_images_image_idx" ON "_project_v_blocks_image_group_images" USING btree ("image_id");
  CREATE UNIQUE INDEX IF NOT EXISTS "_project_v_blocks_image_group_images_locales_locale_parent_id_unique" ON "_project_v_blocks_image_group_images_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_group_order_idx" ON "_project_v_blocks_image_group" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_group_parent_id_idx" ON "_project_v_blocks_image_group" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_project_v_blocks_image_group_path_idx" ON "_project_v_blocks_image_group" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "_project_v_parent_idx" ON "_project_v" USING btree ("parent_id");
  CREATE INDEX IF NOT EXISTS "_project_v_version_version__order_idx" ON "_project_v" USING btree ("version__order");
  CREATE INDEX IF NOT EXISTS "_project_v_version_version_thumbnail_idx" ON "_project_v" USING btree ("version_thumbnail_id");
  CREATE INDEX IF NOT EXISTS "_project_v_version_version_updated_at_idx" ON "_project_v" USING btree ("version_updated_at");
  CREATE INDEX IF NOT EXISTS "_project_v_version_version_created_at_idx" ON "_project_v" USING btree ("version_created_at");
  CREATE INDEX IF NOT EXISTS "_project_v_version_version__status_idx" ON "_project_v" USING btree ("version__status");
  CREATE INDEX IF NOT EXISTS "_project_v_created_at_idx" ON "_project_v" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "_project_v_updated_at_idx" ON "_project_v" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "_project_v_snapshot_idx" ON "_project_v" USING btree ("snapshot");
  CREATE INDEX IF NOT EXISTS "_project_v_published_locale_idx" ON "_project_v" USING btree ("published_locale");
  CREATE INDEX IF NOT EXISTS "_project_v_latest_idx" ON "_project_v" USING btree ("latest");
  CREATE INDEX IF NOT EXISTS "_project_v_autosave_idx" ON "_project_v" USING btree ("autosave");
  CREATE UNIQUE INDEX IF NOT EXISTS "_project_v_locales_locale_parent_id_unique" ON "_project_v_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "payload_folders_name_idx" ON "payload_folders" USING btree ("name");
  CREATE INDEX IF NOT EXISTS "payload_folders_folder_idx" ON "payload_folders" USING btree ("folder_id");
  CREATE INDEX IF NOT EXISTS "payload_folders_updated_at_idx" ON "payload_folders" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "payload_folders_created_at_idx" ON "payload_folders" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_global_slug_idx" ON "payload_locked_documents" USING btree ("global_slug");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_updated_at_idx" ON "payload_locked_documents" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_created_at_idx" ON "payload_locked_documents" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_rels_order_idx" ON "payload_locked_documents_rels" USING btree ("order");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_rels_parent_idx" ON "payload_locked_documents_rels" USING btree ("parent_id");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_rels_path_idx" ON "payload_locked_documents_rels" USING btree ("path");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_rels_users_id_idx" ON "payload_locked_documents_rels" USING btree ("users_id");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_rels_media_id_idx" ON "payload_locked_documents_rels" USING btree ("media_id");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_rels_project_id_idx" ON "payload_locked_documents_rels" USING btree ("project_id");
  CREATE INDEX IF NOT EXISTS "payload_locked_documents_rels_payload_folders_id_idx" ON "payload_locked_documents_rels" USING btree ("payload_folders_id");
  CREATE INDEX IF NOT EXISTS "payload_preferences_key_idx" ON "payload_preferences" USING btree ("key");
  CREATE INDEX IF NOT EXISTS "payload_preferences_updated_at_idx" ON "payload_preferences" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "payload_preferences_created_at_idx" ON "payload_preferences" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "payload_preferences_rels_order_idx" ON "payload_preferences_rels" USING btree ("order");
  CREATE INDEX IF NOT EXISTS "payload_preferences_rels_parent_idx" ON "payload_preferences_rels" USING btree ("parent_id");
  CREATE INDEX IF NOT EXISTS "payload_preferences_rels_path_idx" ON "payload_preferences_rels" USING btree ("path");
  CREATE INDEX IF NOT EXISTS "payload_preferences_rels_users_id_idx" ON "payload_preferences_rels" USING btree ("users_id");
  CREATE INDEX IF NOT EXISTS "payload_migrations_updated_at_idx" ON "payload_migrations" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "payload_migrations_created_at_idx" ON "payload_migrations" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_image_order_idx" ON "main_page_images_blocks_image" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_image_parent_id_idx" ON "main_page_images_blocks_image" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_image_path_idx" ON "main_page_images_blocks_image" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_image_image_idx" ON "main_page_images_blocks_image" USING btree ("image_id");
  CREATE UNIQUE INDEX IF NOT EXISTS "main_page_images_blocks_image_locales_locale_parent_id_unique" ON "main_page_images_blocks_image_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_about_us_order_idx" ON "main_page_images_blocks_about_us" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_about_us_parent_id_idx" ON "main_page_images_blocks_about_us" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_about_us_path_idx" ON "main_page_images_blocks_about_us" USING btree ("_path");
  CREATE UNIQUE INDEX IF NOT EXISTS "main_page_images_blocks_about_us_locales_locale_parent_id_unique" ON "main_page_images_blocks_about_us_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_navigation_order_idx" ON "main_page_images_blocks_navigation" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_navigation_parent_id_idx" ON "main_page_images_blocks_navigation" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_navigation_path_idx" ON "main_page_images_blocks_navigation" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "main_page_images_blocks_navigation_image_idx" ON "main_page_images_blocks_navigation" USING btree ("image_id");
  CREATE INDEX IF NOT EXISTS "main_page_images__status_idx" ON "main_page_images" USING btree ("_status");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_image_order_idx" ON "_main_page_images_v_blocks_image" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_image_parent_id_idx" ON "_main_page_images_v_blocks_image" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_image_path_idx" ON "_main_page_images_v_blocks_image" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_image_image_idx" ON "_main_page_images_v_blocks_image" USING btree ("image_id");
  CREATE UNIQUE INDEX IF NOT EXISTS "_main_page_images_v_blocks_image_locales_locale_parent_id_unique" ON "_main_page_images_v_blocks_image_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_about_us_order_idx" ON "_main_page_images_v_blocks_about_us" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_about_us_parent_id_idx" ON "_main_page_images_v_blocks_about_us" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_about_us_path_idx" ON "_main_page_images_v_blocks_about_us" USING btree ("_path");
  CREATE UNIQUE INDEX IF NOT EXISTS "_main_page_images_v_blocks_about_us_locales_locale_parent_id_unique" ON "_main_page_images_v_blocks_about_us_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_navigation_order_idx" ON "_main_page_images_v_blocks_navigation" USING btree ("_order");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_navigation_parent_id_idx" ON "_main_page_images_v_blocks_navigation" USING btree ("_parent_id");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_navigation_path_idx" ON "_main_page_images_v_blocks_navigation" USING btree ("_path");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_blocks_navigation_image_idx" ON "_main_page_images_v_blocks_navigation" USING btree ("image_id");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_version_version__status_idx" ON "_main_page_images_v" USING btree ("version__status");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_created_at_idx" ON "_main_page_images_v" USING btree ("created_at");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_updated_at_idx" ON "_main_page_images_v" USING btree ("updated_at");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_snapshot_idx" ON "_main_page_images_v" USING btree ("snapshot");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_published_locale_idx" ON "_main_page_images_v" USING btree ("published_locale");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_latest_idx" ON "_main_page_images_v" USING btree ("latest");
  CREATE INDEX IF NOT EXISTS "_main_page_images_v_autosave_idx" ON "_main_page_images_v" USING btree ("autosave");`)
}

export async function down({ db, payload, req }: MigrateDownArgs): Promise<void> {
  await db.execute(sql`
   DROP TABLE "users" CASCADE;
  DROP TABLE "media" CASCADE;
  DROP TABLE "media_locales" CASCADE;
  DROP TABLE "project_blocks_image" CASCADE;
  DROP TABLE "project_blocks_image_locales" CASCADE;
  DROP TABLE "project_blocks_image_group_images" CASCADE;
  DROP TABLE "project_blocks_image_group_images_locales" CASCADE;
  DROP TABLE "project_blocks_image_group" CASCADE;
  DROP TABLE "project" CASCADE;
  DROP TABLE "project_locales" CASCADE;
  DROP TABLE "_project_v_blocks_image" CASCADE;
  DROP TABLE "_project_v_blocks_image_locales" CASCADE;
  DROP TABLE "_project_v_blocks_image_group_images" CASCADE;
  DROP TABLE "_project_v_blocks_image_group_images_locales" CASCADE;
  DROP TABLE "_project_v_blocks_image_group" CASCADE;
  DROP TABLE "_project_v" CASCADE;
  DROP TABLE "_project_v_locales" CASCADE;
  DROP TABLE "payload_folders" CASCADE;
  DROP TABLE "payload_locked_documents" CASCADE;
  DROP TABLE "payload_locked_documents_rels" CASCADE;
  DROP TABLE "payload_preferences" CASCADE;
  DROP TABLE "payload_preferences_rels" CASCADE;
  DROP TABLE "payload_migrations" CASCADE;
  DROP TABLE "main_page_images_blocks_image" CASCADE;
  DROP TABLE "main_page_images_blocks_image_locales" CASCADE;
  DROP TABLE "main_page_images_blocks_about_us" CASCADE;
  DROP TABLE "main_page_images_blocks_about_us_locales" CASCADE;
  DROP TABLE "main_page_images_blocks_navigation" CASCADE;
  DROP TABLE "main_page_images" CASCADE;
  DROP TABLE "_main_page_images_v_blocks_image" CASCADE;
  DROP TABLE "_main_page_images_v_blocks_image_locales" CASCADE;
  DROP TABLE "_main_page_images_v_blocks_about_us" CASCADE;
  DROP TABLE "_main_page_images_v_blocks_about_us_locales" CASCADE;
  DROP TABLE "_main_page_images_v_blocks_navigation" CASCADE;
  DROP TABLE "_main_page_images_v" CASCADE;
  DROP TYPE "public"."_locales";
  DROP TYPE "public"."enum_project_blocks_image_phone_conf_img_align";
  DROP TYPE "public"."enum_project_blocks_image_phone_conf_desc_pos";
  DROP TYPE "public"."enum_project_blocks_image_desk_conf_desc_pos";
  DROP TYPE "public"."enum_project_blocks_image_group_images_phone_conf_img_align";
  DROP TYPE "public"."enum_project_blocks_image_group_images_phone_conf_desc_pos";
  DROP TYPE "public"."enum_project_blocks_image_group_images_desk_conf_desc_pos";
  DROP TYPE "public"."enum_project_blocks_image_group_images_desk_conf_group_align";
  DROP TYPE "public"."enum_project_status";
  DROP TYPE "public"."enum__project_v_blocks_image_phone_conf_img_align";
  DROP TYPE "public"."enum__project_v_blocks_image_phone_conf_desc_pos";
  DROP TYPE "public"."enum__project_v_blocks_image_desk_conf_desc_pos";
  DROP TYPE "public"."enum__project_v_blocks_image_group_images_phone_conf_img_align";
  DROP TYPE "public"."enum__project_v_blocks_image_group_images_phone_conf_desc_pos";
  DROP TYPE "public"."enum__project_v_blocks_image_group_images_desk_conf_desc_pos";
  DROP TYPE "public"."enum__project_v_blocks_image_group_images_desk_conf_group_align";
  DROP TYPE "public"."enum__project_v_version_status";
  DROP TYPE "public"."enum__project_v_published_locale";
  DROP TYPE "public"."enum_main_page_images_blocks_image_phone_config_desc_pos";
  DROP TYPE "public"."enum_main_page_images_blocks_image_desk_config_img_pos";
  DROP TYPE "public"."enum_main_page_images_blocks_image_desk_config_desc_pos";
  DROP TYPE "public"."enum_main_page_images_status";
  DROP TYPE "public"."enum__main_page_images_v_blocks_image_phone_config_desc_pos";
  DROP TYPE "public"."enum__main_page_images_v_blocks_image_desk_config_img_pos";
  DROP TYPE "public"."enum__main_page_images_v_blocks_image_desk_config_desc_pos";
  DROP TYPE "public"."enum__main_page_images_v_version_status";
  DROP TYPE "public"."enum__main_page_images_v_published_locale";`)
}
