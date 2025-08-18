import {
  Box,
  Card,
  CardActionArea,
  CardActions,
  CardMedia,
  Modal,
  Typography,
  useMediaQuery,
} from "@mui/material";
import { TAnimeSimplified } from "../../types/anime.type";
import { generSplit } from "../../utils/genreSplit";
import StarRatings from "react-star-ratings";
import { useState } from "react";
import Carousel from 'react-material-ui-carousel';
import { addLog } from "../../services/log";

export interface IAnimeCard {
  anime: TAnimeSimplified;
  query: string;
}

const modalStyle = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '86vw',
  height: '86vh',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
  overflow: 'auto',
};

export const AnimeCard = ({ anime, query }: IAnimeCard) => {
  const [open, setOpen] = useState(false);
  const isMobile = useMediaQuery("(max-width:600px)");

  const handleClick = async () => {
    const log =  new Date().toISOString() + ";Search.clicked;" + query + ";" + anime.anime_id;
    await addLog(log);
    console.log(log);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Card sx={{ m: 1 }} onClick={handleClick}>
        <CardActionArea
          sx={{
            display: "flex",
            justifyContent: "start",
            alignItems: "center",
          }}
        >
          <CardMedia
            sx={{ width: isMobile ? "100px" : "225px", height: isMobile ? "100px" : "320px" }}
            component="img"
            image={anime.main_pic}
            alt={anime.title}
          />
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              m: 2,
              width: isMobile ? "60vw" : "60%",
            }}
          >
            <Typography variant={isMobile ? "h6" : "h5"} component="div">
              {anime.title}
            </Typography>
            {!isMobile && (
              <>
                <Typography variant="body2" color="text.secondary">
                  {anime.synopsis}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                  {generSplit(anime.genres)}
                </Typography>
              </>
            )}
          </Box>
        </CardActionArea>
        {!isMobile && (
          <CardActions>
            <StarRatings
              rating={Number(anime.score)}
              starRatedColor="gold"
              numberOfStars={10}
              name="rating"
              starDimension="24px"
              starSpacing="2px"
            />
          </CardActions>
        )}
      </Card>

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="anime-modal-title"
        aria-describedby="anime-modal-description"
      >
        <Box sx={modalStyle}>
          <Box sx={{ textAlign: 'center', mb: 2 }}>
            <Carousel>
              {anime.pics.split('|').map((pic, index) => (
                <CardMedia
                  key={index}
                  component="img"
                  sx={{ margin: 'auto', width: '300px', height: '400px' }}
                  image={pic}
                  alt={`Additional pic ${index + 1}`}
                />
              ))}
            </Carousel>
          </Box>
          <Typography id="anime-modal-title" variant="h6" component="h2">
            {anime.title}
          </Typography>
          <Typography id="anime-modal-description" sx={{ mt: 2 }}>
            {anime.synopsis}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Type:</strong> {anime.type}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Source:</strong> {anime.source_type}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Episodes:</strong> {anime.num_episodes}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Status:</strong> {anime.status}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Aired:</strong> {anime.start_date} to {anime.end_date}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Season:</strong> {anime.season}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Studios:</strong> {anime.studios}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Genres:</strong> {generSplit(anime.genres)}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <strong>Score:</strong> {anime.score}
          </Typography>
          <Typography sx={{ mt: 2 }}>
            <a href={anime.anime_url} target="_blank" rel="noopener noreferrer">
              More Info
            </a>
          </Typography>
        </Box>
      </Modal>
    </>
  );
};
