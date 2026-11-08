import typer
from http_command_line_tool.database.session import get_session
from http_command_line_tool.schemas.environment import EnvironmentCreate
from http_command_line_tool.services.environment_services import EnvironmentService

env_app = typer.Typer()

@env_app.command("create")
def create_environment(
    name: str = typer.Argument(..., help="Name of the environment")
):
    if not name:
        raise typer.BadParameter(f"name is missing or invalid, check again")\

    # create that environment in the db
    with get_session() as session:
        data = EnvironmentCreate(name=name)

        result = EnvironmentService.create_environment(data, session)

        typer.echo(f"Environment {result.name} is created!")


@env_app.command("list")
def list_environments():
    with get_session() as session:
        result = EnvironmentService.get_environments_list(session)

        typer.echo(f"List of all the environments")
        for res in result:
            typer.echo(res+"\n")