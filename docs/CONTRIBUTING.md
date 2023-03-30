# Contributing Guide

We appreciate your interest in contributing and making this project better. Before you get started, please read the following guidelines:

## How To Run Locally

1. Fork the repository
2. Clone the repository

##### Environment Variables

3. Create a `.env` file in the root directory and add the following:

```bash
MDB_URL= # Your MongoDB URL here (Password included)
API_KEY= # Your API Key here
API_HOST= # Your API Host here
```

4. Set your MongoDB URL (MDB_URL) to your user environment variables (Windows) or your bash profile (Mac/Linux). This is so that you can access your database from your local machine. If you are using Windows, you can follow [this guide][win]. If you are using Mac/Linux, you can follow [this guide][bash].

**Note:** If you are using Windows, you may need to restart your computer for the changes to take effect.

5. Create a Python Virtual Environment ".venv" in the root directory and activate it. No need to install any dependencies yet. In addtion to this, go to app.py and change the line `request.headers.get('referer') == 'https://adsbmilanalytics.com/':` to `request.headers.get('referer') == 'http://localhost:5173/'`. This is so that you can access the API from your local machine.

##### Install Dependencies

6. Run the following command to install all dependencies:

```bash
npm run init
```

**Note:** Windows Users:

```batch
npm run wininit
```

##### Run the Application

7. Run the following command to start the application:

```bash
npm start
```

Windows Users:

```batch
npm run winstart
```

8. Open your browser and go to `http://localhost:5173/` to view the application.

**Note:** You can run the frontend dev server by running `npm run dev`.

[bash]: https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html
[win]: https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/
