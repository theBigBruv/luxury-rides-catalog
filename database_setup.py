from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, drop_database


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class AutoMaker(Base):
    __tablename__ = 'auto_maker'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(1000))
    thumbnail_picture = Column(String(250))
    banner_picture = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Return object data in easily serializeable format
        return {
           'id': self.id,
           'name': self.name,
           'description': self.description,
           'user_id': self.user_id,
        }


class AutoModel(Base):
    __tablename__ = 'auto_model'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1000))
    thumbnail_picture = Column(String(250))
    auto_maker_id = Column(Integer, ForeignKey('auto_maker.id'))
    auto_maker = relationship(AutoMaker)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'description': self.description,
           'id': self.id,
           'user_id': self.user_id,
           'auto_maker_id': self.auto_maker_id,
        }


class AutoModelImage(Base):
    __tablename__ = 'auto_model_image'

    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False)
    auto_model_id = Column(Integer, ForeignKey('auto_model.id'))
    auto_model = relationship(AutoModel)
    auto_maker_id = Column(Integer, ForeignKey('auto_maker.id'))
    auto_maker = relationship(AutoMaker)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Return object data in easily serializeable format"""
        return {
           'image_url': self.image_url,
           'id': self.id,
           'user_id': self.user_id,
           'auto_maker_id': self.auto_maker_id,
           'auto_model_id': self.auto_model_id,
        }


engine = create_engine('sqlite:///luxuryridescatalog.db')
# if database_exists(engine.url):
# drop_database(engine.url)


Base.metadata.create_all(engine)
