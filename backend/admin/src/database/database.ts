import pg, { QueryResult } from "pg";

const { Pool } = pg;

const pool = new Pool({
    host: process.env.HOST,
    user: process.env.USERNAME,
    password: process.env.PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT ? parseInt(process.env.DB_PORT) : 5432,
});

export async function query(text: string, params: [any] | undefined = undefined): Promise<QueryResult> {
    return await pool.query(text, params);
}
