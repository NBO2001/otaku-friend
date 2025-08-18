import { cleanEnv, port, str } from "envalid";

const validateEnv = () => {
  cleanEnv(process.env, {
    PORT: port(),
    ELASTIC_USER: str(),
    ELASTIC_PASSWORD: str(),
    ELASTIC_ENDPOINT: str(),
  });
};

export default validateEnv;
