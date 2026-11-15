import typer
from http_command_line_tool.database.session import get_session
from http_command_line_tool.schemas.environment import EnvironmentCreate
from http_command_line_tool.schemas.environment_variable import EnvironmentVariableCreate
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


@env_app.command("set")
def set_environment_variable(
    env: str = typer.Argument(..., help="Name of the environment"),
    key: str = typer.Argument(..., help="Key"),
    value: str = typer.Argument(..., help="Value"),
    is_secret: bool = typer.Option(
        False, "--secret", "-s",
        help="Mark this variable as secret"
    )
):
    with get_session() as session:
        env_variable_data = EnvironmentVariableCreate(
            key=key,
            value=value,
            is_secret=is_secret,
            env=env
        )

        env_variable = EnvironmentService.set_environment_variable(
            env_variable_data, session
        )
        if env_variable:
            display_value = "*" * 8 if is_secret else value

            typer.echo(
                f"{Fore.GREEN}✓{Style.RESET_ALL} "
                f"Variable {Fore.CYAN}{key}{Style.RESET_ALL} "
                f"set successfully in {Fore.YELLOW}{env}{Style.RESET_ALL}"
            )

            typer.echo(
                f"  {Fore.WHITE}Value:{Style.RESET_ALL} {display_value}"
            )
        else:
            typer.echo(
                f"{Fore.RED}✗ Error:{Style.RESET_ALL} "
                f"Failed to set variable {Fore.CYAN}{key}{Style.RESET_ALL} "
                f"in {Fore.YELLOW}{env}{Style.RESET_ALL}"
            )


@env_app.command("get")
def get_environment_variable(env: str = typer.Argument(..., help="Name of the environment you want to use"), 
                             key: str = typer.Argument(..., help="Name of the key whose value you want to get")):
    with get_session() as session:
        env_variable_value = EnvironmentService.get_env_variable(env, key, session)

        if env_variable_value:
            typer.echo(
                            f"Variable{Fore.YELLOW}{env}{Style.RESET_ALL}"
                            f"Value{Fore.CYAN}{key} : '{env_variable_value}'{Style.RESET_ALL} "
                        )
            
            
