const functions = require("firebase-functions");
const {exec} = require("child_process");
const winston = require("winston");

const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [new winston.transports.File({filename: "firebase.log"})],
});

const main = exec("python app.py", (error, stdout, stderr) => {
  if (error) {
    logger.error(`exec error: ${error}`);
    return;
  }
  logger.info(`stdout: ${stdout}`);
  logger.error(`stderr: ${stderr}`);
});

exports.main = functions.https.onRequest((request, response) => {
  response.exec(main);
});
