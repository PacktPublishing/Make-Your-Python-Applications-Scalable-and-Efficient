import model
from sqlalchemy.orm import Session
from typing import Optional


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, user: model.User) -> None:
        self.session.add(user)

    def get_by_username(self, username: str) -> Optional[model.User]:
        return self.session.query(
            model.User).filter_by(username=username).first()

    def get_by_email(self, email: model.Email) -> Optional[model.User]:
        return self.session.query(
            model.User).filter_by(email=email).first()

    def list_all(self) -> list[model.User]:
        return self.session.query(model.User).all()


class TweetRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, tweet: model.Tweet) -> None:
        self.session.add(tweet)

    def get_by_id(self, tweet_id: int) -> Optional[model.Tweet]:
        return self.session.query(
            model.Tweet).filter_by(id=tweet_id).one_or_none()

    def list_all(self) -> list[model.Tweet]:
        return self.session.query(model.Tweet).all()
