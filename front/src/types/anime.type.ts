
export interface IAnimeSource {
      anime_id: number;
      anime_url: string;
      title: string;
      synopsis: string;
      main_pic: string;
      type: string;
      source_type: string;
      num_episodes: number;
      status: string;
      start_date: string;
      end_date: string;
      season: string;
      studios: string;
      genres: string;
      score: string;
      score_count: string;
      score_rank: string;
      popularity_rank: number;
      members_count: number;
      favorites_count: number;
      watching_count: number;
      completed_count: number;
      on_hold_count: number;
      dropped_count: number;
      plan_to_watch_count: number;
      total_count: number;
      score_10_count: number;
      score_09_count: number;
      score_08_count: number;
      score_07_count: number;
      score_06_count: number;
      score_05_count: number;
      score_04_count: number;
      score_03_count: number;
      score_02_count: number;
      score_01_count: number;
      clubs: string;
      pics: string;
  }
  
  
  export type TAnimeSimplified = Pick<IAnimeSource, "anime_id" | "anime_url" | "title" | "synopsis" | "num_episodes" | "main_pic" | "pics" | "type" | "source_type" | "season" | "genres" | "status" | "studios" | "start_date" | "end_date" | "score" >
    