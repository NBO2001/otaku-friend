import { Router } from "express";
import logsConstroller from "./logs.constroller";



const logRouter = Router();

logRouter.post("/", logsConstroller.addLog);

export default logRouter;