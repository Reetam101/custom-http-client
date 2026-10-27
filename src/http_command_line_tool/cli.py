import typer
import httpx
import validators
from colorama import Fore, Style
from typing import Annotated

app = typer.Typer()


allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

@app.command()
def pyreq(method: str, url: str, header: Annotated[list[str], typer.Option("--header", "-H")]):
    method = method.upper()
    if method not in allowed_methods:
        print(Fore.RED + "" + method + "is an Invalid Method")
        return

    if not validators.url(url):
        print(Fore.RED + "" + url + "is invalid")
        return

    headers = {}

    if header: 
        for h in header:
            key, separator, value = h.partition(":")

            if not separator or not key.strip():
                print(f"{Fore.RED} Invalid header format")

            headers[key.strip()] = value.strip()

    print(f"Method: {method}")
    print(f"URL: {url}")
    print(headers)
    try:
        with httpx.Client(timeout=10.2) as client:
            response = client.request(method, url, headers=headers)
        print(f"Status {response.status_code}")
        print(response.text)
    except httpx.RequestError as e:
        print(f"{Fore.RED} Request failed: {e}" f"{Style.RESET_ALL}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
