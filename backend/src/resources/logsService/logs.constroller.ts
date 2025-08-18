import { Request, Response } from "express";
import logsService from "./logs.service";



const addLog = async (req: Request, res: Response) => {

    const { log } = req.body;

    const append = await logsService.appendLog(log);

    if(append){
        res.status(200).json(append);
    }else{
        res.status(500).json(append);
    }
}

export default { addLog };