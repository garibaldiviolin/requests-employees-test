# requests-employees-test
This is a stress test script for a REST API (details below) that sends a series of GET/POST/PATCH/DELETE asynchronous requests and then shows some details about the best and worst response times and the total time.
The project uses [aiohttp](https://github.com/aio-libs/aiohttp) (asyncio) for the requests and [python-decouple](https://github.com/henriquebastos/python-decouple) to load the environment variables.

## Objective
The same idea could be accomplished by using an a [Apache JMeter](https://jmeter.apache.org/), but since there are some validations made between each request, the code could become really complicated. That is why Python and aiohttp were chosen.

## REST API
More details about the REST API that is tested by this project can be found here: https://github.com/garibaldiviolin/pythonapi .

## Requirements
- Python 3.8+;
- [pipenv](https://github.com/pypa/pipenv).

## Configuring and Running
1) First, create a `.env` from `local.env` template file;
2) Replace the `API_URL` with the API URL;
3) Just run `python test_api.py` and wait for the results.
