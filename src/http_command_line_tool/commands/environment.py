import typer
from http_command_line_tool.database.session import get_session
from http_command_line_tool.schemas.environment import EnvironmentCreate
from http_command_line_tool.services.environment_services import EnvironmentService
from colorama import Fore, Style

env_app = typer.Typer()

@env_app.command("create")
def create_environment(
    name: str = typer.Argument(..., help="Name of the environment")
):
    if not name:
        raise typer.BadParameter(f"name is missing or invalid, check again")

    # create that environment in the db
    with get_session() as session:
        data = EnvironmentCreate(name=name)

        result = EnvironmentService.create_environment(data, session)

        typer.echo(f"Environment {result.name} is created!")


@env_app.command("list")
def list_environments():
    with get_session() as session:
        result = EnvironmentService.get_environments_list(session)

        if not result:
            typer.echo("No environments found.")
            return

        typer.echo("List of all environments:\n")

        for env in result:
            typer.echo(
                f"Name: {env.name} | "
                f"Active: {'Yes' if env.is_active else 'No'}"
            )

@env_app.command("use")
def use_environment(name: str = typer.Argument(..., help="Name of the environment you want to use")):
    if not name:
        raise typer.BadParameter(f"name is missing")

    with get_session() as session:
        environment = EnvironmentService.set_environment_active(name, session)

        if environment:
            typer.echo(f"Environment {environment.name} is ready to use")
        else:
            typer.echo(f"{Fore.RED} Environment {environment.name} does not exist")

@env_app.command("current")
def show_current_active_environment():
    with get_session() as session:
        env = EnvironmentService.get_current_active_environment(session)

        if env:
            typer.echo(f"Current active environment: {env.name}")
        else:
            typer.echo(f"{Fore.RED} there is no current active environment")


# @env_app.command("set")
# def set_environment_variable(env: str = typer.Argument(..., help="Name of the environment"),
#                              key: str = typer.Argument(..., help="Key"), 
#                              value: str = typer.Argument(..., help="value")):
#     with get_session() as session:
#         env = EnvironmentService.set_environment_variable()
