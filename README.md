# adsb_mil_data

Analytics for military aircraft over ADSB.

**Placeholder website at www.adsbmilanalytics.com**

**How to use:**

Create a .env file with the requirements as set in .env-sample. A further argument is require for the mongodb interaction. Please contact me via the discussions if you wish to obtain this otherwise it'll be kept private.

Linux:

```
./build.sh
````

Windows: Used the same way as linux (Make sure you have Git or a Unix emulator installed, or use the manual method)

ATTENTION: All information here is public.
All you need a valid API key for the ADSB Exchange API at the moment while everything is still in early development. When the project gets deployed to the web in the future this will no longer be a requirement.

**FOR DEVELOPERS**

The current stack is as follows:

Backend: Python(Flask), MongoDB, Google Cloud(WIP)

Middleware: RapidAPI

Frontend: Typescript, React, Vite, Firebase, vanilla CSS for now, I'm not too sure about using Tailwind or PostCSS, may or may not use it in the future

**Current tasks**

Working on deployment and fixing bugs

More features

Creating an Electron app
