from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.base_de_datos import Base


class Actividad(Base):
    __tablename__ = "actividades"

    id: Mapped[int] = mapped_column(primary_key=True)
    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyectos.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    bac: Mapped[float] = mapped_column(nullable=False)
    porcentaje_planificado: Mapped[float] = mapped_column(nullable=False)
    porcentaje_completado: Mapped[float] = mapped_column(nullable=False)
    costo_real: Mapped[float] = mapped_column(nullable=False)