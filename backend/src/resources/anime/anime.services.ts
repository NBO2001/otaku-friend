import configClient from "../elasticsearch/elasticsearch.services"
import { IAnimeSource, TAnimeSimplified } from "./anime.types";
import { estypes } from '@elastic/elasticsearch';

export interface ISearch{
  query: string;
  max_result?: number;
  from?: number;
}

export interface IResposeAnimeSearch{
  animes: IAnimeSource[];
  total: number;
}

const search_ltr = async ({ query, max_result, from }: ISearch): Promise<IResposeAnimeSearch> => {
  try {
    const response = await fetch(`http://python_ltr:5000/search_ltr?from=${from}&size=${max_result}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }), 
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const {animes, took } = await response.json();
  
    const total =  took

    return { animes, total } as IResposeAnimeSearch;
  } catch (error) {
    console.error("Error fetching data:", error);
    return { "animes": [], "total": 0 }
  }
};


const search = async ( {query, max_result, from} : ISearch) => {
    const client = configClient();


    const { hits }: estypes.SearchResponse = await client.search<IAnimeSource>({
        "index": "anime",
        "query": {
          "bool": {
            "should": [
              {
                "match_phrase": {
                  "title": {
                    "query": query,
                    "boost": 5.1
                  }
                }
              },
              {
                "match": {
                  "title": {
                    "query": query,
                    "boost": 8,
                    "operator": "and"
                  }
                }
              },
              {
                "match": {
                  "title": {
                    "query": query,
                    "boost": 1.1
                  }
                }
              },
              {
                "match_phrase": {
                  "synopsis": query
                }
              },
              {
                "rank_feature": {
                  "field": "score",
                  "boost": 3.0
                }
              },
              {
                "rank_feature": {
                  "field": "dropped_count",
                  "boost": 1.2
                }
              },
              {
                "rank_feature": {
                  "field": "score_count",
                  "boost": 3.5
                }
              },
              {
                "rank_feature": {
                  "field": "completed_count",
                  "boost": 2.5
                }
              },
              {
                "rank_feature": {
                  "field": "num_episodes",
                  "boost": 1.9
                }
              }
            ]
          }
        },
        "size": max_result ? max_result : 10,
        "from": from ? from : 0
    });

    const animes: IAnimeSource[] = hits.hits.map( (anime: any) => anime._source)

    const total = hits.total ? (hits.total as any)?.value : 0;
    
    return { animes, total } as IResposeAnimeSearch;
}

const simplifiedVersion = (animes: IAnimeSource[]) => {

    const animesSimplified: TAnimeSimplified[] = animes.map((
        {
            anime_id,
            anime_url,
            title,
            synopsis,
            main_pic,
            type,
            source_type,
            num_episodes,
            status,
            start_date,
            end_date,
            season,
            studios,
            genres,
            score,
            pics,
        }: IAnimeSource) => ({
            anime_id,
            anime_url,
            title,
            synopsis,
            main_pic,
            type,
            source_type,
            num_episodes,
            status,
            start_date,
            end_date,
            season,
            studios,
            genres,
            score,
            pics,
        }));
    return animesSimplified
}

export default { search, simplifiedVersion, search_ltr }