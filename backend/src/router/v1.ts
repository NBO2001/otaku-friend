import { Router } from "express";
import animeRouter from "../resources/anime/anime.router";
import logRouter from "../resources/logsService/logs.router";


const v1 = Router();

v1.use("/anime", animeRouter);
v1.use("/log", logRouter);

export default v1;