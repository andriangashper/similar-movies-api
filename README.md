# Similar Movies API

The Similar Movies API is a project that allows you to discover movies that are similar to a given movie description or to other movies. Additionally, it provides an endpoint (which doesn't have a frontend) for retrieving the nodes and edges connecting all the movies, which can be used for network analysis.

## Overview

The API utilizes the THEMOVIEDB API (https://api.themoviedb.org) to retrieve information about movies. It filters movies in English with a satisfactory grade and vote count, excluding those released before 1980.

After gathering movie data, the project employs the OPENAI API to embed movie descriptions into vector representations. This data is subsequently loaded into a PostgreSQL database.

## Getting Started

To get started with the Similar Movies API, follow these basic steps:

1. Clone the repository to your local machine.

git clone https://github.com/andriangashper/similar-movies-api.git

2. Configure Environmental Variables:

Create a `.env` file in the project root directory and set the following environmental variables:

- `THEMOVIEDB_API_KEY`
- `THEMOVIEDB_API_ACCESS_TOKEN`
- `PGDBUSERNAME`
- `PGDBPWD`
- `PGDBNAME`
- `PGDBHOSTPORT`
- `OPENAI_API_KEY`

Populate these variables with your API keys and database credentials.

3. Build the Docker Image:

Build the Docker image using the provided Dockerfile.

docker build -t similar-movies-api .

4. Run the Docker Container:

Start the Docker container to run the API.

docker run -p 8000:8000 similar-movies-api

5. Access the API:

The API will be available at http://localhost:8000 in your web browser or by making HTTP requests.