from datetime import datetime
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import (
    registry,
    relationship,
    backref,
)


import model


mapper_registry = registry()


emails = Table(
    'emails',
    mapper_registry.metadata,
    Column('address', String(150), primary_key=True),
)

users = Table(
    'users',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(100), nullable=False, unique=True),
    Column('email',  ForeignKey("emails.address")),
    Column('created_at', DateTime, default=datetime.utcnow),
)

follow_table = Table(
    'follow_table',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('following',  ForeignKey("users.id")),
    Column('followers',  ForeignKey("users.id")),
)

tweets = Table(
    'tweets',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id',  ForeignKey("users.id")),
    Column('content', String(140), nullable=False),
    Column('timestamp', DateTime, default=datetime.utcnow),
)

likes = Table(
    'likes',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tweet_id',  ForeignKey("tweets.id")),
    Column('user_id',  ForeignKey("users.id")),
)


def load_mappers():
    mapper_registry.map_imperatively(model.Email, emails)
    users_mapper = mapper_registry.map_imperatively(
        model.User,
        users,
        properties={
            'followers': relationship(
                model.User,
                secondary=follow_table,
                primaryjoin=users.c.id == follow_table.c.following,
                secondaryjoin=users.c.id == follow_table.c.followers,
                backref=backref('following', collection_class=set),
                collection_class=set,
            )
        }
    )
    mapper_registry.map_imperatively(
        model.Tweet,
        tweets,
        properties={
            'user': relationship(
                users_mapper,
                backref='tweets',
            ),
            'likes': relationship(
                users_mapper,
                secondary=likes,
                backref='liked_tweets',
                collection_class=set,
            )
        }
    )
