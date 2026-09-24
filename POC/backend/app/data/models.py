from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SubProcess(Base):
    """Master/benchmark table for the 10 Intake sub-processes.

    cpd/cph are productivity benchmarks (Cases Per Day / Cases Per Hour per FTE)
    taken directly from the client's real workbook. fte_capacity = cpd * target_fte_count,
    matching the client's own formula.
    """

    __tablename__ = "subprocess"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    cpd = Column(Float, nullable=False)
    cph = Column(Float, nullable=False)
    target_fte_count = Column(Integer, nullable=False)
    fte_capacity = Column(Float, nullable=False)

    daily_volumes = relationship("DailyVolume", back_populates="subprocess", cascade="all, delete-orphan")
    daily_fte = relationship("DailyFTE", back_populates="subprocess", cascade="all, delete-orphan")
    daily_prod = relationship("DailyProd", back_populates="subprocess", cascade="all, delete-orphan")


class DailyVolume(Base):
    """Daily incoming receipts (dummy/synthetic) per sub-process."""

    __tablename__ = "daily_volume"

    id = Column(Integer, primary_key=True)
    subprocess_id = Column(Integer, ForeignKey("subprocess.id"), nullable=False)
    date = Column(Date, nullable=False)
    receipts = Column(Integer, nullable=False)

    subprocess = relationship("SubProcess", back_populates="daily_volumes")


class DailyFTE(Base):
    """Actual vs planned headcount per sub-process per day (dummy/synthetic)."""

    __tablename__ = "daily_fte"

    id = Column(Integer, primary_key=True)
    subprocess_id = Column(Integer, ForeignKey("subprocess.id"), nullable=False)
    date = Column(Date, nullable=False)
    actual_fte = Column(Float, nullable=False)
    planned_fte = Column(Float, nullable=False)

    subprocess = relationship("SubProcess", back_populates="daily_fte")


class DailyProd(Base):
    """Completed/processed case counts per sub-process per day (dummy/synthetic)."""

    __tablename__ = "daily_prod"

    id = Column(Integer, primary_key=True)
    subprocess_id = Column(Integer, ForeignKey("subprocess.id"), nullable=False)
    date = Column(Date, nullable=False)
    completed = Column(Integer, nullable=False)

    subprocess = relationship("SubProcess", back_populates="daily_prod")
