from datetime import datetime
import re
from typing import Any


class Email:
    def __init__(self, address: str) -> None:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
            raise ValueError("Invalid email address")
        self.address = address

    def __str__(self) -> str:
        return self.address

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Email) and self.address == other.address

    def __hash__(self) -> int:
        return hash(self.address)


class TweetDTO:
    def __init__(
            self,
            tweet_id: int,
            username: str,
            content: str,
            timestamp: datetime,
            num_likes: int,
    ) -> None:
        self.tweet_id = tweet_id
        self.username = username
        self.content = content
        self.timestamp = timestamp
        self.num_likes = num_likes

    def __str__(self) -> str:
        return f"{self.content} - author: {self.username}"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, TweetDTO) and self.tweet_id == other.tweet_id

    def __hash__(self) -> int:
        return hash(f"{self.tweet_id}_{self.username}")


class User:
    def __init__(self, username: str, email: str) -> None:
        self.username = username
        self.email = Email(email).address
        self.followers = set()  # type: set[User]
        self.following = set()  # type: set[User]
        self.tweets: list = []

    def follow(self, user):
        self.following.add(user)
        user.followers.add(self)

    def unfollow(self, user):
        self.following.discard(user)
        user.followers.discard(self)

    def post_tweet(self, tweet):
        self.tweets.append(tweet)

    def get_feed(self):
        feed = [tweet for user in self.following for tweet in user.tweets]
        feed.extend(self.tweets)
        feed.sort(key=lambda tweet: tweet.timestamp, reverse=True)
        return [
            TweetDTO(
                tweet.id,
                tweet.user.username,
                tweet.content,
                tweet.timestamp,
                len(tweet.likes)
            ) for tweet in feed
        ]

    def __str__(self) -> str:
        return self.username

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, User) and self.username == other.username

    def __hash__(self) -> int:
        return hash(f"{self.username}_{self.email}")


class Tweet:
    def __init__(self, user: User, content: str):
        self.user = user
        self.content = content
        self.timestamp = datetime.now()
        self.likes = set()  # type: set[User]

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.discard(user)

    def __str__(self):
        return f"{self.content} - {self.user.username}"

    def __eq__(self, other: Any) -> bool:
        return all([
            isinstance(other, Tweet),
            self.user == other.user,
            self.content == other.content,
        ])
