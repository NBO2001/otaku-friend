import { Request, Response } from "express";
import animeServices from "./anime.services";
import { IQueryAnime, TAnimeSimplified } from "./anime.types";
import { sanitizeString } from "../../utils/sanitizeString";

export interface IReadWithPag{
    from?: number;
    size?: number;
}

export interface IResposeAnimeRead{
    animes: TAnimeSimplified[];
    total: number;
}

const read = async (req: Request, res: Response) => {
    try{
        const { from, size }:IReadWithPag = req.query
        const { query, simplified_version } = req.body as IQueryAnime;

        const cleadQuery = sanitizeString(query);
        
        const animes_ = await animeServices.search({ query: cleadQuery, from, max_result: size });

        if(simplified_version){
            const animes_simplified: IResposeAnimeRead = {
                animes: animeServices.simplifiedVersion(animes_.animes),
                total: animes_.total
            }
            res.status(200).json( animes_simplified )
        }else{
            res.status(200).json(animes_);
        }

    }
    catch (err){
        res.status(400).json(err);
    }

}

const readWithLtr = async (req: Request, res: Response) => {
    try{
        const { from, size }:IReadWithPag = req.query
        const { query } = req.body as IQueryAnime;

        const cleadQuery = sanitizeString(query);
        
        const animes_ = await animeServices.search_ltr({ query: cleadQuery, from, max_result: size });
        
        if(animes_.total>0){
            res.status(200).json({
                animes: animes_.animes,
                total: animes_.total
            });
        }else{
            return await read(req, res);
        }

    }
    catch (err){
        res.status(400).json(err);
    }

}


const readControl = async (req: Request, res: Response) => {
    const isLtr = req.query.ltr=="true" ? true : false;

    if(isLtr) return readWithLtr(req, res);
    else return read(req, res);
}



export default {read,readWithLtr,readControl};