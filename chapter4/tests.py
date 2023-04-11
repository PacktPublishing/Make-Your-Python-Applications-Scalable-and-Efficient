import pytest
from domain import User, Tweet, Email, TweetDTO


def test_user_follow_and_unfollow():
    alice = User(1, "alice", "alice@example.com")
    bob = User(2, "bob", "bob@example.com")

    alice.follow(bob)
    assert alice in bob.followers
    assert bob in alice.following

    alice.unfollow(bob)
    assert alice not in bob.followers
    assert bob not in alice.following


def test_email_validation():
    with pytest.raises(ValueError):
        Email("invalid_email")

    valid_email = Email("valid@example.com")
    assert str(valid_email) == "valid@example.com"


def test_post_tweet_and_get_feed():
    alice = User(1, "alice", "alice@example.com")
    bob = User(2, "bob", "bob@example.com")
    charlie = User(3, "charlie", "charlie@example.com")

    alice.follow(bob)
    alice.follow(charlie)

    tweet1 = Tweet(1, alice, "Hello, world!")
    tweet2 = Tweet(2, bob, "Hi, Alice!")
    tweet3 = Tweet(3, charlie, "Good morning, everyone!")

    alice.post_tweet(tweet1)
    bob.post_tweet(tweet2)
    charlie.post_tweet(tweet3)

    alice_feed = alice.get_feed()
    assert len(alice_feed) == 3
    assert alice_feed[0] == TweetDTO(
        3, "charlie", "Good morning, everyone!", tweet3.timestamp, 0)
    assert alice_feed[1] == TweetDTO(
        2, "bob", "Hi, Alice!", tweet2.timestamp, 0)
    assert alice_feed[2] == TweetDTO(
        1, "alice", "Hello, world!", tweet1.timestamp, 0)


def test_tweet_like_and_unlike():
    alice = User(1, "alice", "alice@example.com")
    bob = User(2, "bob", "bob@example.com")
    tweet = Tweet(1, alice, "Hello, world!")

    tweet.like(bob)
    assert bob in tweet.likes
    assert alice not in tweet.likes

    tweet.unlike(bob)
    assert bob not in tweet.likes
    assert alice not in tweet.likes
