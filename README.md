# AIPlearning

Take home assessment and learning project. A simple web-app served by a react frontend and flask backend.

## Installation

This app uses docker to containerize images for the frontend and backend. If you already have docker installed, simply cd into root and run docker-compose up on terminal with Windows Powershell.

Powershell

```
docker-compose up
```

Otherwise, you can use `setup.ps1` to automatically install and compose the images.

Powershell:

```
.\setup.ps1
```

The backend and frontend should automatically start running once they have been composed. If you need to run either app manually, use:

```
//Run the backend
docker run -it aiplearning-server

//Run the frontend
docker run -it aiplearning-web
```

Or use Docker Desktop and run from the UI directly.

## Usage

Once the frontend and backend service are running, open up a browser and go to http://localhost:5173

Since the submission uses development versions of both frontend and backend, requests between frontend and backend are being logged on their respective terminals.

From the react app, you may try uploading a video with the upload button on the top left of the page. Uploaded videos will show up as buttons labelled by name on the list below the search bar - click on them to see video details.

You can search for videos by filename or detected objects. Search queries are only sent to the backend once you click the Submit button.

> [!CAUTION]
> This app is poorly made. Uploading wrong file types or extremely large files will probably break it. If that happens, a server restart on the backend may be required.

## Testing

### Backend

To test the backend, you will have to bash into the container running the backend by opening a new terminal and performing:

```
docker run -it aiplearning-server bash
```

Inside the container:

```
root@abcdefg:/app# python -m pytest
```

### Frontend

No tests were written for the frontend :/
