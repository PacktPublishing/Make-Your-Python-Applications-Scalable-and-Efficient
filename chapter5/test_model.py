import model
from sqlalchemy import text


def test_load_email(session):
    session.execute(
        text('''INSERT INTO emails (address) VALUES
        ("test1@test.com"),
        ("test2@test.com"),
        ("test3@test.com")''')
    )
    expected = [
        model.Email("test1@test.com"),
        model.Email("test2@test.com"),
        model.Email("test3@test.com"),
    ]
    assert session.query(model.Email).all() == expected


def test_create_email(session):
    e = model.Email("test_create1@test.com")
    session.add(e)
    session.commit()
    assert session.query(model.Email).first() == e


def test_load_user(session):
    session.execute(
        text('''INSERT INTO users (username, email) VALUES
        ("test1", "test1@test.com"),
        ("test2", "test2@test.com"),
        ("test3", "test3@test.com")''')
    )
    expected = [
        model.User('test1', 'test1@test.com'),
        model.User('test2', 'test2@test.com'),
        model.User('test3', 'test3@test.com'),
    ]
    assert session.query(model.User).all() == expected


def test_create_user(session):
    u = model.User('test1', 'test1@test.com')
    session.add(u)
    session.commit()
    assert session.query(model.User).first() == u


def test_user_following(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')
    user_3 = model.User('test3', 'test3@test.com')

    user_1.follow(user_2)
    user_1.follow(user_3)
    session.add(user_1)
    session.add(user_2)
    session.add(user_3)
    session.commit()
    query = session.query(model.User).filter_by(id=user_1.id).one()
    assert len(query.following) == 2
    assert user_2, user_3 in query.following
    assert len(query.followers) == 0


def test_user_followers(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')
    user_3 = model.User('test3', 'test3@test.com')

    user_2.follow(user_1)
    user_3.follow(user_1)
    session.add(user_1)
    session.add(user_2)
    session.add(user_3)
    session.commit()
    query = session.query(model.User).filter_by(id=user_1.id).one()
    assert len(query.followers) == 2
    assert user_2, user_3 in query.followers
    assert len(query.following) == 0


def test_user_unfollow(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')

    user_1.follow(user_2)
    session.add(user_1)
    session.add(user_2)
    session.commit()
    query = session.query(model.User).filter_by(id=user_1.id).one()
    assert len(query.following) == 1
    assert user_2 in query.following
    assert len(query.followers) == 0

    user_1.unfollow(user_2)
    session.commit()

    query = session.query(model.User).filter_by(id=user_1.id).one()
    assert len(query.following) == 0
    assert user_2 not in query.following
    assert len(query.followers) == 0


def test_create_tweet(session):
    user_1 = model.User('test1', 'test1@test.com')
    session.add(user_1)
    session.commit()

    t1 = model.Tweet(user_1, 'it is a first test')
    t2 = model.Tweet(user_1, 'it is a second test')
    session.add(t1)
    session.add(t2)
    session.commit()
    expected = [t1, t2]

    assert session.query(model.Tweet).all() == expected


def test_like_dislike_tweet(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')
    user_3 = model.User('test3', 'test3@test.com')
    session.add(user_1)
    session.add(user_2)
    session.add(user_3)
    session.commit()

    t1 = model.Tweet(user_1, 'it is a test')
    t1.like(user_2)
    t1.like(user_3)
    session.add(t1)
    session.commit()
    query = session.query(model.Tweet).first()
    assert len(query.likes) == 2
    assert user_2, user_3 in query.likes

    t1.unlike(user_2)
    session.commit()
    query = session.query(model.Tweet).first()
    assert len(query.likes) == 1
    assert user_3 in query.likes
    assert user_2 not in query.likes


def test_feed(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')
    user_1.follow(user_2)
    t1 = model.Tweet(user_1, 'it my on message')
    t2 = model.Tweet(user_2, 'it is the first user_1 message')
    t3 = model.Tweet(user_2, 'it is the second user_1 message')
    session.add(user_1)
    session.add(user_2)
    session.add(t1)
    session.add(t2)
    session.add(t3)
    session.commit()
    query = session.query(model.User)
    query_user_1 = query.filter_by(id=user_1.id).one()
    query_user_2 = query.filter_by(id=user_2.id).one()
    assert len(query_user_1.get_feed()) == 3
    assert len(query_user_2.get_feed()) == 2
    assert isinstance(query_user_1.get_feed()[0], model.TweetDTO)
    assert query_user_1.get_feed()[0].content == t3.content
