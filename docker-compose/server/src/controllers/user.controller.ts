import { Request, Response } from "express";
import pool from "../config/db";

export async function register(req: Request, res: Response) {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: "Nome e e-mail são obrigatórios" });
  }
  
  try {
    const result = await pool.query(
      "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
      [name, email]
    );
    if (result.rows.length !== 0) {
      res.status(201).json(result.rows[0]);
    } else {
      res.status(400).json({ error: "Problemas ao criar o usuário" });
    }
  } catch (err: any) {
    res.status(400).json({ error: err.message });
  }
}

export async function getAll(_: Request, res: Response) {
  try {
    const result = await pool.query("SELECT * FROM users ORDER BY name");
    res.status(200).json(result.rows);
  } catch (err: any) {
    res.status(400).json({ error: err.message });
  }
}