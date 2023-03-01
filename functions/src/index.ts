import * as functions from "firebase-functions";

export const API_URL = functions.https.onRequest((request, response) => {
  const allowedOrigins = ["https://adsbmilanalytics.com", "https://www.adsbmilanalytics.com"];

  if (allowedOrigins.includes(request.headers.origin as string)) {
    response.set("Access-Control-Allow-Origin", request.headers.origin);
    response.send(process.env.API_URL);
  } else {
    response.status(403).send("Forbidden");
  }
});
