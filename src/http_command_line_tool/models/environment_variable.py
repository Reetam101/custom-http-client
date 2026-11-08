from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base import Base

class EnvironmentVariable(Base):
    __tablename__ = "environment_variables"

    id: Mapped[int] = mapped_column(primary_key=True)

    key: Mapped[str] = mapped_column(String(100), nullable=False)

    value: Mapped[str] = mapped_column(String, nullable=False)

    is_secret: Mapped[bool] = mapped_column(Boolean, default=False)

    environment_id: Mapped[int] = mapped_column(ForeignKey("environments.id"))

    environment: Mapped["Environment"] = relationship("Environment", back_populates="variables")