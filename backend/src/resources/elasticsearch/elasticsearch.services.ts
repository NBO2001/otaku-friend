import { Client } from '@elastic/elasticsearch'


const configClient = () => {

    const client = new Client({ node: `${process.env.ELASTIC_ENDPOINT}`, auth: {
        username: `${process.env.ELASTIC_USER}`,
        password: `${process.env.ELASTIC_PASSWORD}`
    } });

    return client;
}


export default configClient;