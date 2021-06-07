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

* [Visual Studio Code](https://code.visualstudio.com/): This is far and away the best free IDE available, and with the right extensions, it can be made to outperform a lot of paid ones, too. Some relevant extensions I use are [Docker](https://www.docker.com/products/docker-desktop) and [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance).
* [Prospector](https://pypi.org/project/prospector/): The linter requested for this project.
* [Docker](https://www.docker.com/): The entire app lives in Docker containers managed using the Docker Desktop app for Windows.
* [Docker Compose](https://docs.docker.com/compose/): This is used to set up a virtual development environment to host all of the servers the application utilizes in order to function.
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

1. [Install Python](https://www.python.org/downloads/).
2. [Install Docker](https://docs.docker.com/get-docker/).
3. [Install Docker Compose](https://docs.docker.com/compose/install/).
    * **!!**: If you are on Mac or Windows and have installed Docker Desktop, you don't need to worry about installing Docker Compose, as it comes with Docker Desktop. Only Linux users need to worry about this step.
4. Clone this repository onto your machine.
5. Head to [CoinMarketCap](https://coinmarketcap.com/api/) and sign up for a developer account. You can select the Basic plan, which is free and provides 333 daily credits (with a monthly maximum of 10,000 credits). Each call for financial information on 100 cryptocurrencies or fewer will count as a single credit, as will a query for metadata on all of the cryptocurrencies that are on the platform.

## Setting Up the Local Python Environment

Once you have everything installed, you will have to set up your Python environment.

1. Go into the repository on your machine, and `cd` into the backend directory.
2. Run the command `pipenv shell` to set up a virtual environment in the backend directory.
3. Run the command `pipenv install --dev` to install the dependencies.
4. Run the command `pip freeze > requirements.txt`. This will update your requirements document with all of the necessary dependencies to use this application.

Note that any time you install new packages not listed here, you will have to perform step 4 again in order to update your requirements.txt file with all of the necessary dependencies. Then, you must also rebuild the Docker images with the `docker compose up --build` command. See the **Building Up and Tearing Down the Docker Containers** section below for more information.

## Setting Up the Config File

I have provided a sample config file in this repository, but it will take a little work to get it ready to use. Here's the code inside the [sample_config.py](backend/src/sample_config.py) file:

```python
username = '<Your MongoDB username.>'
password = '<Your MongoDB password.>'
database = '<The name of the MongoDB database you are using.>'
api_key = '<Your CoinMarketCap API key.>'

task_ignore_result = False
timezone = 'UTC'

beat_schedule = {
    'update_watchlist': {
        'task': 'main.update_watchlist_prices',
        'schedule': 30.0
    }
}
```

The first thing you will have to do will be to rename the file to `config.py`. Make sure it is still in the backend/src directory.

Any of the text in `<angle brackets>` above should be replaced with whatever it says. So, your username will be your MongoDB username, your api_key will be your personal API key from CoinMarketCap, and so on.

If you wish, you can change the frequency with which the database will be updated with current financial information for your watchlist. I would recommend keeping it at 30 seconds, since updating it more frequently doesn't seem to provide new information. You may instead choose to update it *less* frequently, if you intend to keep the server up for a while. At a refresh rate of 30 seconds, you will exhaust your daily 333 credits for the Basic plan in just under 3 hours from database updates alone.

Apart from these values, I wouldn't recommend updating anything.

## Building Up and Tearing Down the Docker Containers

This app is using Docker Compose, so once everything is installed and set up, the `docker-compose.yml` file should have everything the application needs to dockerize itself using just three commands.

1. From the root directory of the project, run the command `docker compose up --build`. This will build the images for the first time, install all of the dependencies in your requirements.txt file, and launch the application.
2. Whenever you would like to build the application after the first time, you can use `docker compose up` instead.
3. To bring down the application, use `Ctrl+C` inside the terminal to stop the server. Once it is down, use the command `docker compose down` to dismount it from Docker.

## Running Tests Locally

Once everything is set up, the tests are simple to run.

1. From the root directory of the project, `cd` into the backend directory.
2. Run the command `pipenv run pytest` to run the tests.
3. Assuming everything has been set up correctly, all 5 tests should pass as they are currently written.

## Future Improvements

Below is a list of improvements that I wanted to add into the application, but haven't yet had the time to do. These should make their way into the project in the near future.

* Make more of the app asynchronous.
    * I wanted to make the database update that happens upon launch an asynchronous task, but it proved too challenging to implement in the time allotted.
    * A few of the application functions were prime candidates for asyncio's Tasks. Namely, these were the `update_coin_list` and `update_watchlist` functions in the [database](backend/src/database.py) module.
* I would have liked to have spent more time exploring Pydantic. I tend to prefer static languages, so working with libraries that provide type hints and data validation in dynamic languages like Python only serve to make me that much more comfortable.
* I had originally intended for the application to have a frontend made using either [Dash](https://plotly.com/dash/) or [Elm](https://elm-lang.org/).
* Had I more time, and had accomplished a frontend, I would have standardized the format the API uses to return information, likely using ResponseModel.
* Another stretch goal that would have been useful would be to send log data to InfluxDB.
* I wrote pydocs comments for the application, but something I will be adding later will be a CI/CD pipeline to generate FastAPI docs and push them to GitHub.
* More tests are always welcome, so another idea I had was to create a mock-up coin API in order to do more automated testing without having to rely on the CoinMarketCap API.
* Relying on the requirements.txt file is probably suboptimal since there could be conflicts between that and the Pipfile.lock. A better way would be to have pipenv install the dependencies directly, but I have so far been unable to get it to work in the Dockerfile.
