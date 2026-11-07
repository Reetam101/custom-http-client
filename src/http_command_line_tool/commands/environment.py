import typer

env_app = typer.Typer()

@env_app.command("create")
def create_environment(
    name: str = typer.Argument(..., help="Name of the environment")
):
    typer.echo(f"Creating environment... {name}")

