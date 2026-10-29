import typer
import httpx
import validators
from colorama import Fore, Style
from typing import Annotated
import json

app = typer.Typer()


allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

def convert_to_number(num: str) -> int | float | str | ValueError:
    try:
        return int(num)
    except ValueError:
        try:
            return float(num)
        except ValueError:
            return num


@app.command()
def pyreq(method: str, url: str, header: Annotated[list[str], typer.Option("--header", "-H")] = None, query: Annotated[list[str], typer.Option("--query", "-q")] = None, json_body: Annotated[str, typer.Option("--json")] = None):
    method = method.upper()
    if method not in allowed_methods:
        print(Fore.RED + "" + method + "is an Invalid Method")
        return

    if not validators.url(url):
        print(Fore.RED + "" + url + "is invalid")
        return

    headers = {}
    queries = {}
    data = {}
    if header: 
        for h in header:
            key, separator, value = h.partition(":")

            if not separator or not key.strip():
                print(f"{Fore.RED} Invalid header format")

            headers[key.strip()] = value.strip()
        print(headers)


    if query:
        for q in query:
            key, separator, value = q.partition("=")

            if not separator or not key.strip():
                print(f"{Fore.RED} Invalid query format")

            queries[key.strip()] = convert_to_number(value.strip())
        print(queries)
  
    if method == 'POST' or method == 'PUT' or method == 'PATCH':
        if json_body:
            data = json.loads(json_body)


    print(f"Method: {method}")
    print(f"URL: {url}")
    try:
        with httpx.Client(timeout=10.2) as client:
            response = client.request(method, url, headers=headers, params=queries, json=data)
            duration_in_seconds = response.elapsed.total_seconds()
        print(f"Status code: {response.status_code}")
        print(f"URL: {response.url}")
        # print(response.content)
        print(f"Content size: {response.headers.get('Content-Length', 0)} bytes")
        print(f"Duration: {duration_in_seconds * 1000}ms")
    except httpx.RequestError as e:
        print(f"{Fore.RED} Request failed: {e}" f"{Style.RESET_ALL}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
