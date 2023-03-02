# adsb_mil_data

Analytics for military aircraft over ADSB.

**Placeholder website at www.adsbmilanalytics.com**

**How to use:**

1. Get an API key from ADSB Exchange (https://www.adsbexchange.com/data/)
2. Set your environment variables with said key and host with the following names:

```API_KEY``` and ```HOST```

3. Run the following command in the root directory of the project:

```build.sh``` 

4. Then ```cd client``` and run ```npm run dev```

5. Then ```cd ../server``` and run ```python3 main.py```

6. Go to ```localhost:5173``` in your browser

**Notes**

This project is still in early development and is not yet deployed to the web. If you want to use it, you will need to run it locally for now.

This project is also not yet optimized for mobile devices.

MongoDB is used for the database. You will need to configure your own MongoDB instance and set the environment variable ```MDB_URL``` to the URI of your MongoDB instance and adjust the collections and database names accordingly.

Windows: Used the same way as linux (Make sure you have Git or a Unix emulator installed, or use the manual method)

**Stack**

Backend: Python(Flask), MongoDB, Google Cloud App Engine

Frontend: Typescript, React, Vite, Firebase, vanilla CSS

**Current tasks**

Bug fixes and optimizations

Various admin tasks and security updates. At the moment the site is secure on the surface such as cross site scripting but there are some other vulnerabilities that need to be addressed. Not to mention a privacy policy, and a terms of service need to be written.

More features

**Questions?**

Feel free to contact me at support@adsbmilanalytics.com