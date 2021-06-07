# stelligent-demo

This application is a proof-of-concept for a customizable cryptocurrency dashboard. It allows the user to search a database of cryptocurrencies and create watchlist of those that interest them. Their watchlist provides current financial and portfolio information on the cryptocurrencies in their watchlist. They can also insert a transaction record, a purchase or a sell, and see a summary of their portfolio that includes data like their current investment's value and the profit they've made so far, on both a per-cryptocurrency and overall scale.

## Endpoints

* `GET /`
    * Returns the user's watchlist.
* `POST /watch`
    * Adds a cryptocurrency to the user's watchlist.
    * Request Body: `Watch`
* `DELETE /watch`
    * Removes a cryptocurrency from the user's watchlist.
    * Request Body: `Watch`
* `POST /buy`
    * Adds a purchase record to the user's transaction history.
    * Request Body: `Transaction`
* `POST /sell`
    * Adds a sell record to the user's transaction history.
    * Request Body: `Transaction`
* `GET /records`
    * Returns the user's complete transaction history.
* `GET /records/{coin_name}`
    * Returns the user's transaction history for the provided cryptocurrency.
    * Path Parameters:
        * `coin_name`: The common name for the cryptocurrency.
* `GET /summary`
    * Returns a complete summary for the user's cryptocurrency investment portfolio.
* `GET /summary/{coin_name}`
    * Returns a summary for the user's investment portfolio concerning a particular cryptocurrency.
    * Path Parameters:
        * `coin_name`: The common name for the cryptocurrency.

## Technology Used

Below is a list of all the important technology used in the production of this app.

### Development Environment

* [Visual Studio Code](https://code.visualstudio.com/): This is far and away the best free IDE available, and with the right extensions, it can be made to outperform a lot of paid ones, too. Some relevant extensions I use are [Docker]() and [Pylance]().
* [Prospector](https://pypi.org/project/prospector/): The linter requested for this project.
* [Docker](https://www.docker.com/): The entire app lives in Docker containers managed using the Docker Desktop app for Windows.
* [pipenv](https://pipenv.pypa.io/en/latest/): My virtual environment and package manager of choice.
* [Trello](https://trello.com/): My personal kanban board for the project lives here.

### Code Quality &amp; Continuous Integration

* [CircleCI](https://circleci.com/): I created a job that performed unit tests and ensured their passing after a commit was pushed to GitHub. Since the application is currently hosted locally, there isn't much more that can be done with it, but it will come in handy when it comes time to deal with deployment.
* [githooks](https://git-scm.com/docs/githooks): A fairly simple pre-commit githook ran unit tests, and blocked the commit if the tests failed. While this didn't happen to me during this project (thankfully), it would certainly have prevented me from damaging my main branch in the event of a particularly grievous oversight on my part.

### Python Modules/Libraries

* [Aiohttp](https://docs.aiohttp.org/en/stable/): This library was used to make asynchronous HTTP requests with...
* [Asyncio](https://docs.python.org/3/library/asyncio.html): Most of the app's activities have been made asynchronous. Those that haven't are on the Future Plans (details below).
* [Celery](https://docs.celeryproject.org/en/stable/index.html): I used this to create a scheduled task that periodically updates the database with current financial information for cryptocurrencies on the user's watchlist.
* [FastAPI](https://fastapi.tiangolo.com/): This was the framework that was used to make the API endpoints for the app.
* [MongoEngine](http://mongoengine.org/): I used MongoEngine to map objects to the database as documents.
* [Pydantic](https://pydantic-docs.helpmanual.io/): I used this library to create BaseModels for the API in order to achieve some level of data validation.
* [Pytest](https://docs.pytest.org/en/6.2.x/): The testing library I used to write unit tests for the business logic module.
* [Uvicorn](https://www.uvicorn.org/): This was the server that supported the app's entire backend.

### External Services

* [CoinMarketCap API](https://coinmarketcap.com/api/): The API I chose to use for providing cryptocurrency information. The Basic level is free, and permits 333 "credits" (typically a call with less than 100 coins on it will cost a single credit) per day, and up to 10,000 "credits" per month. It has a much more limited suite of information available, but for this proof of concept, it is more than sufficient.
* [MongoDB](https://www.mongodb.com/): The MongoDB database holds a list of all cryptocurrencies available on the market (per CoinMarketCap), the user's watchlist, and the user's transaction history.
* [MongoExpress](https://github.com/mongo-express/mongo-express): The admin interface I used to interact with the database.
* [RabbitMQ](https://www.rabbitmq.com/): I used this as the broker for Celery.

## Requirements

Software that needs to be installed. Python, Docker, docker-compose, pipenv.

Required accounts for the API.

## Setup

How to set up local Python environment

## How to set up the config file

.

## Building and Breaking the Docker App

Starting up and tearing down the docker compose.

## Running Tests Locally

.

## Future Improvements

Below is a list of improvements that I wanted to add into the application, but haven't yet had the time to do. These should make their way into the project in the near future.

* Make more of the app asynchronous.
    * I wanted to make the database update that happens upon launch an asynchronous task, but it proved too challenging to implement in the time allotted.
    * A few of the application functions were prime candidates for asyncio's Tasks. Namely, these were the `update_coin_list` and `update_watchlist` functions in the [database](backend/src/database.py) module.
* I would have liked to have spent more time exploring Pydantic. I tend to prefer static languages, so working with libraries that provide type hints and data validation in dynamic languages like Python only serve to make me that much more comfortable.
* I had originally intended for the application to have a frontend made using either [Dash](https://plotly.com/dash/) or [Elm](https://elm-lang.org/).
* Had I more time, and had accomplished a frontend, I would have standardized the information the API returns, likely using ResponseModel.
* Another stretch goal that would have been useful would be to send log data to InfluxDB.
* I wrote pydocs comments for the application, but something I will be adding later will be a CI/CD pipeline to generate FastAPI docs and push them to GitHub.
* More tests are always welcome, so another idea I had was to create a mock-up coin API in order to do more automated testing without having to rely on the CoinMarketCap API.
