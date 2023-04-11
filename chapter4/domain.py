import datetime
import re


class Email:
    def __init__(self, address):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
            raise ValueError("Invalid email address")
        self.address = address

    def __str__(self):
        return self.address

    def __eq__(self, other):
        return isinstance(other, Email) and self.address == other.address

    def __hash__(self):
        return hash(self.address)


class TweetDTO:
    def __init__(self, tweet_id, username, content, timestamp, num_likes):
        self.tweet_id = tweet_id
        self.username = username
        self.content = content
        self.timestamp = timestamp
        self.num_likes = num_likes

    def __str__(self):
        return f"{self.content} - author: {self.username}"

    def __eq__(self, other):
        return isinstance(other, TweetDTO) and self.tweet_id == other.tweet_id

    def __hash__(self):
        return hash(f"{self.tweet_id}_{self.username}")


class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = Email(email)
        self.followers = set()
        self.following = set()
        self.tweets = []

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
                tweet.tweet_id,
                tweet.user.username,
                tweet.content,
                tweet.timestamp,
                len(tweet.likes)
            ) for tweet in feed
        ]


class Tweet:
    def __init__(self, tweet_id, user, content):
        self.tweet_id = tweet_id
        self.user = user
        self.content = content
        self.timestamp = datetime.datetime.now()
        self.likes = set()

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.discard(user)

    def __str__(self):
        return f"{self.content} - {self.user.username}"


if __name__ == '__main__':
    # Create users
    alice = User(1, "alice", "alice@example.com")
    bob = User(2, "bob", "bob@example.com")
    charlie = User(3, "charlie", "charlie@example.com")

    # Users follow each other
    alice.follow(bob)
    alice.follow(charlie)
    bob.follow(alice)

    # Users post tweets
    alice.post_tweet(Tweet(1, alice, "Hello, world!"))
    bob.post_tweet(Tweet(2, bob, "Hi, Alice!"))
    charlie.post_tweet(Tweet(3, charlie, "Good morning, everyone!"))

    # Display the feed of each user
    for user in [alice, bob, charlie]:
        print(f"{user.username}'s feed:")
        for tweet in user.get_feed():
            print(tweet)
        print()
