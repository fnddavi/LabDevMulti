import express, {Request, Response} from "express";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.get("/", function(_req: Request, res: Response) {
  res.json({ message: "Rota funcionando corretamente!" });
});

app.listen(port, function () {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
