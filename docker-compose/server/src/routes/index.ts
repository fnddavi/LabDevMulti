import {Router, Request, Response} from "express";
import { getAll, register } from "../controllers/user.controller";

const router = Router();

router.post("/", register);
router.get("/", getAll);

export default router;