import { TAnimeSimplified } from "../types/anime.type";
import api from "./api";

export interface IResposeAnimeRead{
  animes: TAnimeSimplified[];
  total: number;
}

export interface ISearch{
  query: string;
  from?: number;
}

export const search = async ({query, from}: ISearch) => {
  try {

    const {data} = await api.post(`/anime?from=${from ? from : 0}&size=5`, {
      query,
      "simplified_version": true
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 5000 
    });
    const data_: IResposeAnimeRead = data;
    
    return data_;

  } catch (err) {
    console.error(err)
    return {animes: [], total: 0} as IResposeAnimeRead ;
  }
};
