from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    preferences = relationship("Preference", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float)

    user = relationship("User", back_populates="preferences")

if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///netflix.db", echo=True)
    Base.metadata.create_all(bind=engine)
    print("Veritabanı oluşturuldu.")