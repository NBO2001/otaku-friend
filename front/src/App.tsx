import { useState } from "react";
import {
  Box,
  Container,
  IconButton,
  InputBase,
  Pagination,
  Paper,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { IResposeAnimeRead, search } from "./services/anime";
import { AnimeCard } from "./components/AnimeCard/AnimeCard";
import { TAnimeSimplified } from "./types/anime.type";
import Footer from "./components/Footer/Footer";
import * as React from "react";
import { alpha } from "@mui/material";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { addLog } from "./services/log";

function App() {
  const [inputAnime, setInputAnime] = useState("");
  const [animes, setAnimes] = useState<TAnimeSimplified[] | null>(null);
  const [pages, setPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [ nowQuery, setNowQuery ] = useState("");

  const handleSearch = async (page: number = 1) => {
    const from = (page - 1) * 5;
    const animes_: IResposeAnimeRead = await search({
      query: inputAnime,
      from,
    });
    
    setAnimes(animes_.animes);
    setPages(
      Math.ceil(animes_.total / 5) < 5 ? Math.ceil(animes_.total / 5) : 5
    );
    setNowQuery(inputAnime);

    const ids = animes_?.animes?.map( (anime) => anime.anime_id);
    const documents = ids?.join("|")

    const log =  new Date().toISOString() + ";Search.viewed;" + inputAnime + ";" + documents;
    await addLog(log);
    console.log(log);
    
    

    setCurrentPage(page);
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    handleSearch();
  };

  const handlePageChange = (
    event: React.ChangeEvent<unknown>,
    page: number
  ) => {
    handleSearch(page);
  };



  return (
    <>
      <Box
        id="hero"
        sx={(theme) => ({
          width: "100%",
          backgroundImage:
            theme.palette.mode === "light"
              ? "linear-gradient(180deg, #CEE5FD, #FFF)"
              : `linear-gradient(#02294F, ${alpha("#090E10", 0.0)})`,
          backgroundSize: "100% 20%",
          backgroundRepeat: "no-repeat",
        })}
      >
        <Container
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            pt: { xs: 14, sm: 20 },
            pb: { xs: 8, sm: 12 },
          }}
        >
          <Stack
            spacing={2}
            useFlexGap
            sx={{ width: { xs: "100%", sm: "70%" } }}
          >
            <Typography
              variant="h1"
              sx={{
                display: "flex",
                flexDirection: { xs: "column", md: "row" },
                alignSelf: "center",
                textAlign: "center",
                fontSize: "clamp(3.5rem, 10vw, 4rem)",
                color: (theme) =>
                  theme.palette.mode === "light"
                    ? "primary.main"
                    : "primary.light",
              }}
            >
              Search Animes
            </Typography>

            <Typography
              textAlign="center"
              color="text.secondary"
              sx={{ alignSelf: "center", width: { sm: "100%", md: "80%" } }}
            >
              Explore our anime search engine and discover a vast collection of
              amazing titles. Whether you're a fan of action, romance, fantasy,
              or any other genre, our search tool is here to help you find the
              best animes that match your preferences. Start your journey now
              and dive into the captivating world of anime with ease and speed.
              <Paper
                component="form"
                sx={{
                  p: "2px 4px",
                  display: "flex",
                  alignItems: "center",
                  margin: "0 auto",
                  mt: 5,
                }}
                onSubmit={handleSubmit}
              >
                <InputBase
                  sx={{ ml: 1, flex: 1 }}
                  placeholder="Search Animes"
                  inputProps={{ "aria-label": "search anime" }}
                  value={inputAnime}
                  onChange={(e) => setInputAnime(e.target.value)}
                />
                <IconButton
                  type="submit"
                  sx={{ p: "10px" }}
                  aria-label="search"
                >
                  <SearchIcon />
                </IconButton>
              </Paper>
            </Typography>
          </Stack>
        </Container>
      </Box>
      <Container>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            minHeight: "100vh",
            pt: 2,
          }}
        >
          {animes &&
            animes.map((anime: TAnimeSimplified) => (
              <AnimeCard key={anime.anime_id} anime={anime} query={nowQuery}/>
            ))}

          {animes && (
            <Box sx={{ mt: 1, mb: 2 }}>
              <Pagination
                count={pages}
                color="primary"
                page={currentPage}
                onChange={handlePageChange}
                size="medium"
              />
            </Box>
          )}
        </Box>
      </Container>
      <Footer />
    </>
  );
}

export default App;
