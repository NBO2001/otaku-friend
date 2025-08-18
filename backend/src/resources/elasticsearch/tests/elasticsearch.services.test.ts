import { Client } from '@elastic/elasticsearch';
import configClient from '../elasticsearch.services';
import {jest} from '@jest/globals';

jest.mock('@elastic/elasticsearch', () => {
    return {
        Client: jest.fn()
    };
});

describe('configClient', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        process.env.ELASTIC_ENDPOINT = 'http://localhost:9200';
        process.env.ELASTIC_USER = 'elastic_user';
        process.env.ELASTIC_PASSWORD = 'elastic_password';
    });

    it('should configure the client with the correct endpoint and auth details', () => {
        configClient();

        expect(Client).toHaveBeenCalledWith({
            node: 'http://localhost:9200',
            auth: {
                username: 'elastic_user',
                password: 'elastic_password'
            }
        });
    });

    it('should return an instance of Client', () => {
        const client = configClient();

        expect(client).toBeInstanceOf(Client);
    });
});
