from http_command_line_tool.schemas.environment import EnvironmentCreate, EnvironmentResponse
from http_command_line_tool.models.environment import Environment
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select, update

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


        
