import asyncio
from decouple import config
from time import monotonic

from aiohttp import ClientSession, ClientTimeout

request_times = dict()

API_URL = config("API_URL")


def get_employee_payload(name):
    """Builds the employee payload based on the name informed."""
    return {
        "name": str(name),
        "age": 42,
        "city": "Tokyo"
    }


def get_employee_urls(params):
    """Builds the API URLs for GET/POST/PUT/PATCH/DELETE HTTP methods.
    """
    return (
        f"{API_URL}/employees/",
        f"{API_URL}/employees/{params['name']}/",
    )


def async_call(model, url_method, http_method, payload_method, channel_slug):
    """Fetch list of web pages asynchronously."""
    start_time = monotonic()

    loop = asyncio.get_event_loop()  # event loop
    future = asyncio.ensure_future(
        create_call_async(
            url_method,
            http_method,
            payload_method,
            params
        )
    )  # tasks to do
    loop.run_until_complete(future)  # loop until done

    print(
        'Async {} {} time={:.03f} seconds'.format(
            model,
            http_method.upper(),
            monotonic() - start_time
        )
    )


async def create_call_async(url_method, http_method, payload_method, params):
    """Launch requests for all web pages."""
    tasks = []

    name_position = 0

    async with ClientSession(timeout=ClientTimeout(total=0)) as session:
        for name in range(name_position, name_position + 100):
            params["name"] = name
            urls = url_method(params)
            data = payload_method(name) if payload_method else {}

            task = asyncio.ensure_future(
                create_request_async(
                    data, http_method, session, urls)
            )
            tasks.append(task)  # create list of tasks
        _ = await asyncio.gather(*tasks)  # gather task responses


async def create_request_async(data, http_method, session, urls):
    """Fetch a url, using specified ClientSession."""
    global request_times
    start = monotonic()

    if http_method == "post":
        methods_test = [
            ("post", 201, urls[0]),
            ("get", 200, urls[1]),
            ("patch", 200, urls[1]),
            ("get", 200, urls[1]),
            ("delete", 204, urls[1]),
            ("get", 404, urls[1]),
        ]
    else:
        methods_test = [
            ("get", 200, urls[0])
        ]

    has_deleted = False

    for method_test, expected_status_code, url in methods_test:
        method = getattr(session, method_test)

        if method_test == "patch":
            data["city"] = "New York City"
            del data["name"]

        async with method(url, json=data) as response:
            resp = await response.read()
            resp = resp

            if http_method not in request_times:
                request_times[http_method] = list()
            request_times[http_method].append(monotonic() - start)

            if response.status != expected_status_code:
                print(
                    "Response status={}, method={}, "
                    "error={} request data={}".format(
                        response.status, method_test, resp, data
                    )
                )

            if method_test == "delete":
                has_deleted = True

            if not has_deleted:
                response_json = await response.json()
                if response_json["city"] != data["city"]:
                    breakpoint()
                    print(
                        f"Invalid city={response_json['city']}, "
                        "expected={data['city']} for name={data['name']}"
                    )


start = monotonic()

params = {}
async_call(
    "Employees",
    get_employee_urls,
    "post",
    get_employee_payload,
    params,
)

end = monotonic()

print("All process time={:.03f} seconds".format(end - start))
