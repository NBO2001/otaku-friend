import express, { NextFunction, Request, Response } from "express";
import dotenv from "dotenv";
import cors from "cors";
import router from "./router";
import validateEnv from "./utils/validateEnv";
import { logger } from "./middleware/logger";

dotenv.config();

validateEnv();

const app = express();
const PORT = process.env.PORT ?? 4444;

const corsOptions = {
  origin: "*", 
  methods: "GET,HEAD,PUT,PATCH,POST,DELETE",
  allowedHeaders: "Content-Type,Authorization",
};


app.use(cors(corsOptions));

app.use(express.json());

app.use(logger('completo'));

// Use the router for API routes
app.use("/api", router);

app.listen(PORT, () => {
  console.log(`Running on port: ${PORT}`);
});
