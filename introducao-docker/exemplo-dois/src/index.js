const express = require("express");
const dotenv = require("dotenv");

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.get("/", function (_req, res) {
  res.json({ message: "Rota para projeto JS!" });
});

app.listen(port, function () {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
