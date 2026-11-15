from http_command_line_tool.schemas.environment import EnvironmentCreate, EnvironmentResponse
from http_command_line_tool.models.environment import Environment
from http_command_line_tool.models.environment_variable import EnvironmentVariable
from http_command_line_tool.schemas.environment_variable import EnvironmentVariableCreate, EnvironmentVariableResponse
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select, update
from colorama import Fore, Style


class EnvironmentService:
    def create_environment(data: EnvironmentCreate, session: Session) -> EnvironmentResponse:
        environment = Environment(name=data.name)

        session.add(environment)
        session.commit()
        session.refresh(environment)

        return EnvironmentResponse.model_validate(environment)

    def get_environments_list(session: Session) -> List[EnvironmentResponse]:
        stmt = select(Environment)

        all_envs = session.scalars(stmt).all()

        result = [
            EnvironmentResponse.model_validate(env)
            for env in all_envs
        ]
        return result

    def set_environment_active(name: str, session: Session):
        stmt = select(Environment).where(Environment.name == name)
        env = session.execute(stmt).scalar_one_or_none()

        if not env:
            return None
        
        stmt2 = (
            update(Environment).where(
                Environment.is_active == True,
                Environment.name != name
            ).values(is_active=False)
        )
        session.execute(stmt2)
        env.is_active = True
        session.commit()
        session.refresh(env)
        return env

    def get_current_active_environment(session: Session):
        stmt = select(Environment).where(Environment.is_active == True)

        active_env = session.execute(stmt).scalar_one_or_none()

        if not active_env:
            return None

        return active_env

    def set_environment_variable(data: EnvironmentVariableCreate, session: Session):
        data_dict = data.model_dump()

        environment_id = session.execute(select(Environment.id).where(Environment.name == data.env)).scalar_one_or_none()

        if environment_id is None:
            raise ValueError(f"{Fore.RED} Environment '{data.env}' not found")

        data_dict.pop("env")

        env_variable = EnvironmentVariable(**data_dict, environment_id=environment_id)

        session.add(env_variable)
        session.commit()
        session.refresh(env_variable)

        return env_variable

    def get_env_variable(env_name: str, key: str, session: Session):
        stmt1 = select(Environment.id).where(Environment.name == env_name)
        environment_id = session.execute(stmt1).scalar_one_or_none()

        if environment_id is None:
            raise ValueError(f"{Fore.RED} Environment '{env_name}' does not exist yet")

        env_variable_value = session.execute(select(EnvironmentVariable.value).where(EnvironmentVariable.environment_id == environment_id, EnvironmentVariable.key == key)).scalar_one_or_none()

        if env_variable_value is None:
            raise ValueError(f"{Fore.RED} Key '{key}' doesn't exist in the environment '{env_name}'")

        return env_variable_value
        







        
