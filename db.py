from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Price(Base):
    __tablename__ = "crypto_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(5))
    price: Mapped[float]
    timestamp: Mapped[float]

    def _jsonify(self):
        return {'id':self.id, 'ticker':self.ticker, 'price':self.price, 'timestamp': self.timestamp}

    def __repr__(self) -> str:
        return f"Price(id={self.id!r}, ticker={self.ticker!r}, price={self.price!r}, timestamp={self.timestamp!r})"

engine = create_engine("sqlite:///prices.db", echo=True)
Base.metadata.create_all(engine)