import express from "express";
import { query } from "./database/database.js";

const app = express();

const port = process.env.PORT || 3000;

app.get("/", async (req, res) => {
});

app.listen(port);
