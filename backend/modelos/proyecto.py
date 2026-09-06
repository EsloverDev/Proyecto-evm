from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.base_de_datos import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
