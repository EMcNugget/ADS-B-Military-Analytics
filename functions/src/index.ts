import * as functions from "firebase-functions";

export const API_URL = functions.https.onRequest((request, response) => {
  const allowedOrigins = ["https://adsbmilanalytics.com", "https://www.adsbmilanalytics.com"];

  if (allowedOrigins.includes(request.headers.origin as string)) {
    response.set("Access-Control-Allow-Origin", request.headers.origin);
    response.set("Access-Control-Allow-Methods", "GET, POST");
    response.set("Access-Control-Allow-Headers", "Content-Type");
    response.set("Access-Control-Allow-Credentials", "true");
    response.send(process.env.API_URL);
  } else {
    response.status(403).send("Forbidden");
  }
});
