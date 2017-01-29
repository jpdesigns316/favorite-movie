
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    picture = Column(String)

    def __init__(self, name, email, picture):
        self.name = name
        self.email = email
        self.picture = picture

class Movies(Base):
    __tablename__ = 'movie-info'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    year = Column(Integer, nullable=False)
    released = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    runtime = Column(Integer, nullable=False)
    plot = Column(Text, nullable=False)
    metascore = Column(Float)
    imdb_score = Column(Float)
    rottentomatoes_rating = Column(Float)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'released': self.released,
            'genre': self.genre,
            'runtime': self.runtime,
            'plot': self.plot,
            'metascore': self.metascore,
            'imdb_score': self.imdb_score,
            'rottentomatoes_rating': self.rottentomatoes_rating,
            'user_id': self.user_id
        }

class TV_Shows(Base):
    __tablename__ = 'tv-info'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    year = Column(Integer, nullable=False)
    released = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    runtime = Column(Integer, nullable=False)
    plot = Column(Text, nullable=False)
    metascore = Column(Float)
    imdb_score = Column(Float)
    rottentomatoes_rating = Column(Float)
    total_seasons = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'released': self.released,
            'genre': self.genre,
            'runtime': self.runtime,
            'plot': self.plot,
            'metascore': self.metascore,
            'imdb_score': self.imdb_score,
            'rottentomatoes_rating': self.rottentomatoes_rating,
            'total_seasons': self.total_seasons,
            'user_id': self.user_id
        }

# Commment out the line that referes to the database you are using
engine = create_engine('sqlite:///movies.db')
#engine = create_engine('mysql://root:6bJI%!IEsm#41@q9@localhost/movie_db')
#engine = create_engine('postgresql://movie:x2X&D3Nb!Lz8Mw4q@localhost/movies')

Base.metadata.create_all(engine)
