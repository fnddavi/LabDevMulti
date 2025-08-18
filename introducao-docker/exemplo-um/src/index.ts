import express, { Request, Response } from "express";
import dotenv from "dotenv";
import fs from "fs";
import path from "path";

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.get("/", function (_req: Request, res: Response) {
  res.json({ message: "Rota funcionando corretamente!" });
});

app.listen(port, function () {
  console.log(`Servidor rodando em http://localhost:${port}`);
});

// Middleware para registrar IP e horário da requisição
app.use((req: Request, _: Response, next) => {
  const ip = req.ip || req.socket.remoteAddress || "IP não identificado";
  const dataHora = new Date().toISOString();
  const log = `IP: ${ip} - Data/Hora: ${dataHora}\n`;
  const logPath = path.join(__dirname, "logs.txt");
  fs.appendFile(logPath, log, (err) => {
    if (err) {
      console.error("Erro ao gravar log:", err);
    }
  });
  next();
});

