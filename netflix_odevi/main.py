from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Movie, Preference
from pydantic import BaseModel
import pandas as pd
from sklearn.cluster import KMeans

app = FastAPI()

# Veritabanı bağlantısı
DATABASE_URL = "sqlite:///netflix.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Netflix öneri sistemi API çalışıyor!"}

# Kullanıcı ekleme  

class UserCreate(BaseModel):
    name: str

@app.post("/users/")
def add_user(user: UserCreate):
    db = SessionLocal()
    new_user = User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "name": new_user.name}

# Film ekleme
class MovieCreate(BaseModel):
    title: str
    genre: str

@app.post("/movies/")
def add_movie(movie: MovieCreate):
    db = SessionLocal()
    new_movie = Movie(title=movie.title, genre=movie.genre)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return {
        "id": new_movie.id,
        "title": new_movie.title,
        "genre": new_movie.genre
    }

# Tercih ekleme 
class PreferenceCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: float

@app.post("/preferences/")
def add_preference(preference: PreferenceCreate):
    db = SessionLocal()
    new_pref = Preference(
        user_id=preference.user_id,
        movie_id=preference.movie_id,
        rating=preference.rating
    )
    db.add(new_pref)
    db.commit()
    db.refresh(new_pref)
    return {
        "id": new_pref.id,
        "user_id": new_pref.user_id,
        "movie_id": new_pref.movie_id,
        "rating": new_pref.rating
    }

# ------------------ ÖNERİ SİSTEMİ ------------------
@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int):
    db = SessionLocal()

    # Tüm tercih verilerini çek
    prefs = db.query(Preference).all()
    data = [{
        "user_id": p.user_id,
        "movie_id": p.movie_id,
        "rating": p.rating
    } for p in prefs]

    df = pd.DataFrame(data)

    if df.empty or user_id not in df["user_id"].unique():
        return {"recommended_movies": []}

    # Kullanıcı-film matrisini oluştur
    user_movie_matrix = df.pivot_table(index="user_id", columns="movie_id", values="rating").fillna(0)

    # KMeans ile kümeleme yap
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    user_movie_matrix["cluster"] = kmeans.fit_predict(user_movie_matrix)

    # Mevcut kullanıcının kümesini al
    user_cluster = user_movie_matrix.loc[user_id, "cluster"]

    # Aynı kümedeki kullanıcıları bul
    similar_users = user_movie_matrix[user_movie_matrix["cluster"] == user_cluster].index.tolist()

    # Kullanıcının izlediği filmler
    watched = df[df["user_id"] == user_id]["movie_id"].tolist()

    # Önerilecek filmleri filtrele
    similar_prefs = df[df["user_id"].isin(similar_users)]
    recommendations = similar_prefs[~similar_prefs["movie_id"].isin(watched)]

    # En çok beğenilen 3 filmi öner
    top_movies = recommendations.groupby("movie_id")["rating"].mean().sort_values(ascending=False).head(3).index.tolist()

    # Film adlarını al
    movie_titles = db.query(Movie).filter(Movie.id.in_(top_movies)).all()
    return {"recommended_movies": [m.title for m in movie_titles]}

