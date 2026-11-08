from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


from ..database.base import Base

class Environment(Base):
    __tablename__ = "environments"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    variables: Mapped[list["EnvironmentVariable"]] = relationship("EnvironmentVariable", back_populates="environment", cascade="all, delete-orphan")
    