# Fast API ToDo List with JWT authentication

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/gomofficial/social-media.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/Scripts/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ uvicorn main:app
```

And navigate to `http://127.0.0.1:8000/`.

## Running Locally with Docker

1.build the image:

```sh
  $ docker-compose build .
```
2.Spin up the containers
```sh
  $ docker-compose up
```

then view the site at  http://localhost:8000/ 

## API Docs 
  navigate to `http://127.0.0.1:8000/docs/`

## Features
 rest api using fastapi,
 jwt authentications
