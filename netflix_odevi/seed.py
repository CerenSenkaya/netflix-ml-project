from models import Base, User, Movie, Preference
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///netflix.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
db = Session()

# Kullanıcılar
users = [User(name="Ali"), User(name="Zeynep"), User(name="Mert")]
db.add_all(users)
db.commit()

# Filmler
movies = [
    Movie(title="Inception", genre="Sci-Fi"),
    Movie(title="Titanic", genre="Romance"),
    Movie(title="The Matrix", genre="Action"),
    Movie(title="Coco", genre="Animation"),
]
db.add_all(movies)
db.commit()

# Tercihler (rating)
prefs = [
    Preference(user_id=1, movie_id=1, rating=5.0),
    Preference(user_id=1, movie_id=2, rating=3.5),
    Preference(user_id=2, movie_id=1, rating=4.5),
    Preference(user_id=2, movie_id=3, rating=4.0),
    Preference(user_id=3, movie_id=4, rating=5.0),
    Preference(user_id=3, movie_id=2, rating=2.5),
]
db.add_all(prefs)
db.commit()

print("Test verileri başarıyla eklendi.")
