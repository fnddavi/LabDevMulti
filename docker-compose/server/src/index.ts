import express, {Request, Response} from "express";
import router from "./routes";  
import dotenv from "dotenv";
import cors from "cors";

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

app.use("/api", router);

app.use(function(_:Request, res:Response) {
  res.status(404).json({ error: "Rota não encontrada" });
});

app.listen(port, function () {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
