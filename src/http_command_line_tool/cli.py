import typer
import httpx
import validators
from colorama import Fore, Style
from typing import Annotated
import json
import base64
from http_command_line_tool.commands.environment import env_app


app = typer.Typer()

app.add_typer(env_app, name="env")

allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
allowed_auth = ["basic", "bearer-token", "api-key"]

def convert_to_number(num: str) -> int | float | str | ValueError:
    try:
        return int(num)
    except ValueError:
        try:
            return float(num)
        except ValueError:
            return num

def encode_basic_auth(username: str, password: str) -> str:
    credentials = f"{username}:{password}"

    encoded_credentials = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("ascii")

    return f"Basic {encoded_credentials}"


@app.command()
def pyreq(method: str, url: str, header: Annotated[list[str], typer.Option("--header", "-H")] = None, query: Annotated[list[str], typer.Option("--query", "-q")] = None, json_body: Annotated[str, typer.Option("--json")] = None, form: Annotated[list[str], typer.Option("--form", "-F")]=None, auth: Annotated[str, typer.Option("--auth")] = None, username: Annotated[str, typer.Option("--username")] = None, password: Annotated[str, typer.Option("--password")] =None, token: Annotated[str, typer.Option("--token")] = None, api_key: Annotated[str, typer.Option("--api-key")] = None, api_key_name: Annotated[str, typer.Option("--api-key-name")] = None, ):
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
    files = {}
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
            headers["Content-Type"] = "application/json"
            data = json.loads(json_body)

        if form:
            headers["Content-Type"] = "multipart/form-data"
            for item in form:
                key, separator, value = item.partition("=")

                if not separator or not key.strip():
                    raise typer.BadParameter(
                        f"Invalid form field: {item}"
                    )
                if value.startswith('@'):
                    file_path = value[1:]

                    try:
                        files[key.strip()] = open(file_path, "rb")
                    except OSError as exc:
                        raise typer.BadParameter(f"Cannot open file path: {file_path}") from exc
                else:
                    data[key.strip()] = value 


    if auth.lower() not in allowed_auth:
        raise typer.BadParameter(f"Invalid auth type: {auth} provide from : {allowed_auth}")
    else:
        # Basic username and password auth
        if auth.lower() == "basic":
            if not username or not password:
                raise typer.BadParameter(f"Invalid or Missing credentials")
            encoded = encode_basic_auth(username=username, password=password)
            headers['Authorization'] = encoded

        # Bearer token auth
        if auth.lower() == "bearer-token":
            if not token:
                raise typer.BadParameter(f"Token is invalid or not passed")
            headers['Authorization'] = f"Bearer {token}"

        # API key auth
        if auth.lower() == "api-key":
            if not api_key or not api_key_name:
                raise typer.BadParameter(f"Invalid or Missing api-key and api-key-name")
            headers[api_key_name] = api_key


    print(f"Method: {method}")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    try:
        with httpx.Client(timeout=10.2) as client:
            response = client.request(method, url, params=queries, data=data, files=files, headers=headers)
            duration_in_seconds = response.elapsed.total_seconds()
        print(f"Status code: {response.status_code}")
        print(f"URL: {response.url}")
        print(f"Content size: {response.headers.get('Content-Length', 0)} bytes")
        print(f"Duration: {duration_in_seconds * 1000}ms")
        print(response.content)
    except httpx.RequestError as e:
        print(f"{Fore.RED} Request failed: {e}" f"{Style.RESET_ALL}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
