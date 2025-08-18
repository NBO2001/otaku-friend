import { Response, Request, NextFunction } from 'express';
import fs from 'fs/promises';

class Logger {
  private pathLog: string = process.env.PATHLOG || '';
  private filePath: string = `./${this.pathLog}/logis.log`;

  public getFilePath(): string {
    return this.filePath;
  }

  public async appendInFile(message: string) {
    try {
      await fs.appendFile(this.getFilePath(), message);
    } catch (error) {
      console.log(`Error while trying to write to ${this.getFilePath()}`);
      console.error(error);
    }
  }
}

const loggerBasic = async (req: Request, res: Response, next: NextFunction) => {
  const logMessage = `${new Date().toISOString()}, ${req.url}, ${req.method}\n`;

  console.log(logMessage)

  next();
};

const loggerFull = async (req: Request, res: Response, next: NextFunction) => {
    const logMessage: string = `${new Date().toISOString()}, ${req.url}, ${req.method}, ${req.httpVersion}, ${req.get('User-Agent')}\n`;
    console.log(logMessage)


    next();
};

const defaultFunction = (req: Request, res: Response, next: NextFunction) =>
  next();

export const logger = (type: string) => {
  if (type === 'simples') return loggerBasic;
  else if (type === 'completo') return loggerFull;
  else return defaultFunction;
};