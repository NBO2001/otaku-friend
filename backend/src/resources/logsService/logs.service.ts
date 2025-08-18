const fs = require('fs/promises');
const path = require('path');

const appendLog = async (logLine: string) => {
  const logFilePath = path.join(__dirname, '../../../logging/search.log');

  const logEntry = `${logLine}\n`;

  try{

    await fs.appendFile(logFilePath, logEntry);
    return true;

  }catch(err){
    console.log(err)
    return false;
  }

};

export default { appendLog };
