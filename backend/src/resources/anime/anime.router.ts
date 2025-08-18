import { Router } from "express";
import animeController from "./anime.controller";



const animeRouter = Router();

animeRouter.post("/", animeController.readControl);

export default animeRouter;