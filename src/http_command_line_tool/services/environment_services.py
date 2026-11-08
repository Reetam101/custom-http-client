from http_command_line_tool.schemas.environment import EnvironmentCreate, EnvironmentResponse
from http_command_line_tool.models.environment import Environment
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select

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

        return all_envs
        
