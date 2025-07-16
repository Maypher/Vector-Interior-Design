import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

export async function up({ db, payload, req }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
   CREATE TABLE "project_blocks_animated_text" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"text_color" varchar DEFAULT '#101214',
  	"block_name" varchar
  );
  
  CREATE TABLE "project_blocks_animated_text_locales" (
  	"text" varchar,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" varchar NOT NULL
  );
  
  CREATE TABLE "_project_v_blocks_animated_text" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"text_color" varchar DEFAULT '#101214',
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE "_project_v_blocks_animated_text_locales" (
  	"text" varchar,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  CREATE TABLE "main_page_images_blocks_animated_text" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" varchar PRIMARY KEY NOT NULL,
  	"text_color" varchar DEFAULT '#101214',
  	"block_name" varchar
  );
  
  CREATE TABLE "main_page_images_blocks_animated_text_locales" (
  	"text" varchar,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" varchar NOT NULL
  );
  
  CREATE TABLE "_main_page_images_v_blocks_animated_text" (
  	"_order" integer NOT NULL,
  	"_parent_id" integer NOT NULL,
  	"_path" text NOT NULL,
  	"id" serial PRIMARY KEY NOT NULL,
  	"text_color" varchar DEFAULT '#101214',
  	"_uuid" varchar,
  	"block_name" varchar
  );
  
  CREATE TABLE "_main_page_images_v_blocks_animated_text_locales" (
  	"text" varchar,
  	"id" serial PRIMARY KEY NOT NULL,
  	"_locale" "_locales" NOT NULL,
  	"_parent_id" integer NOT NULL
  );
  
  ALTER TABLE "project_blocks_animated_text" ADD CONSTRAINT "project_blocks_animated_text_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."project"("id") ON DELETE cascade ON UPDATE no action;
  ALTER TABLE "project_blocks_animated_text_locales" ADD CONSTRAINT "project_blocks_animated_text_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."project_blocks_animated_text"("id") ON DELETE cascade ON UPDATE no action;
  ALTER TABLE "_project_v_blocks_animated_text" ADD CONSTRAINT "_project_v_blocks_animated_text_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_project_v"("id") ON DELETE cascade ON UPDATE no action;
  ALTER TABLE "_project_v_blocks_animated_text_locales" ADD CONSTRAINT "_project_v_blocks_animated_text_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_project_v_blocks_animated_text"("id") ON DELETE cascade ON UPDATE no action;
  ALTER TABLE "main_page_images_blocks_animated_text" ADD CONSTRAINT "main_page_images_blocks_animated_text_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."main_page_images"("id") ON DELETE cascade ON UPDATE no action;
  ALTER TABLE "main_page_images_blocks_animated_text_locales" ADD CONSTRAINT "main_page_images_blocks_animated_text_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."main_page_images_blocks_animated_text"("id") ON DELETE cascade ON UPDATE no action;
  ALTER TABLE "_main_page_images_v_blocks_animated_text" ADD CONSTRAINT "_main_page_images_v_blocks_animated_text_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_main_page_images_v"("id") ON DELETE cascade ON UPDATE no action;
  ALTER TABLE "_main_page_images_v_blocks_animated_text_locales" ADD CONSTRAINT "_main_page_images_v_blocks_animated_text_locales_parent_id_fk" FOREIGN KEY ("_parent_id") REFERENCES "public"."_main_page_images_v_blocks_animated_text"("id") ON DELETE cascade ON UPDATE no action;
  CREATE INDEX "project_blocks_animated_text_order_idx" ON "project_blocks_animated_text" USING btree ("_order");
  CREATE INDEX "project_blocks_animated_text_parent_id_idx" ON "project_blocks_animated_text" USING btree ("_parent_id");
  CREATE INDEX "project_blocks_animated_text_path_idx" ON "project_blocks_animated_text" USING btree ("_path");
  CREATE UNIQUE INDEX "project_blocks_animated_text_locales_locale_parent_id_unique" ON "project_blocks_animated_text_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX "_project_v_blocks_animated_text_order_idx" ON "_project_v_blocks_animated_text" USING btree ("_order");
  CREATE INDEX "_project_v_blocks_animated_text_parent_id_idx" ON "_project_v_blocks_animated_text" USING btree ("_parent_id");
  CREATE INDEX "_project_v_blocks_animated_text_path_idx" ON "_project_v_blocks_animated_text" USING btree ("_path");
  CREATE UNIQUE INDEX "_project_v_blocks_animated_text_locales_locale_parent_id_unique" ON "_project_v_blocks_animated_text_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX "main_page_images_blocks_animated_text_order_idx" ON "main_page_images_blocks_animated_text" USING btree ("_order");
  CREATE INDEX "main_page_images_blocks_animated_text_parent_id_idx" ON "main_page_images_blocks_animated_text" USING btree ("_parent_id");
  CREATE INDEX "main_page_images_blocks_animated_text_path_idx" ON "main_page_images_blocks_animated_text" USING btree ("_path");
  CREATE UNIQUE INDEX "main_page_images_blocks_animated_text_locales_locale_parent_id_unique" ON "main_page_images_blocks_animated_text_locales" USING btree ("_locale","_parent_id");
  CREATE INDEX "_main_page_images_v_blocks_animated_text_order_idx" ON "_main_page_images_v_blocks_animated_text" USING btree ("_order");
  CREATE INDEX "_main_page_images_v_blocks_animated_text_parent_id_idx" ON "_main_page_images_v_blocks_animated_text" USING btree ("_parent_id");
  CREATE INDEX "_main_page_images_v_blocks_animated_text_path_idx" ON "_main_page_images_v_blocks_animated_text" USING btree ("_path");
  CREATE UNIQUE INDEX "_main_page_images_v_blocks_animated_text_locales_locale_parent_id_unique" ON "_main_page_images_v_blocks_animated_text_locales" USING btree ("_locale","_parent_id");`)
}

export async function down({ db, payload, req }: MigrateDownArgs): Promise<void> {
  await db.execute(sql`
   DROP TABLE "project_blocks_animated_text" CASCADE;
  DROP TABLE "project_blocks_animated_text_locales" CASCADE;
  DROP TABLE "_project_v_blocks_animated_text" CASCADE;
  DROP TABLE "_project_v_blocks_animated_text_locales" CASCADE;
  DROP TABLE "main_page_images_blocks_animated_text" CASCADE;
  DROP TABLE "main_page_images_blocks_animated_text_locales" CASCADE;
  DROP TABLE "_main_page_images_v_blocks_animated_text" CASCADE;
  DROP TABLE "_main_page_images_v_blocks_animated_text_locales" CASCADE;`)
}
