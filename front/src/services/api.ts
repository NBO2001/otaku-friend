import axios from "axios";

const api = axios.create({
  baseURL: `${process.env.REACT_APP_ANIME_API_ENDPOINT}/api/v1`,
});

export default api;
