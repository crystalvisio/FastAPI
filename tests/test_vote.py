import pytest
from app import models


# Fixture for an existing upvote
@pytest.fixture()
def test_existing_upvote(test_create_posts, test_user, session):
    new_vote = models.Vote(post_id=test_create_posts[3].id, user_id=test_user["id"], vote_dir=1)
    session.add(new_vote)
    session.commit()


# Fixture for an existing downvote
@pytest.fixture()
def test_existing_downvote(test_create_posts, test_user, session):
    new_vote = models.Vote(post_id=test_create_posts[2].id, user_id=test_user["id"], vote_dir=0)
    session.add(new_vote)
    session.commit()


# Testing Route for Upvote
def test_upvote(authorize_client, test_create_posts):
    post_id = test_create_posts[3].id
    res = authorize_client.post("/vote", json={"post_id": post_id, "vote_dir": 1})
    
    assert res.status_code == 201
    assert res.json() == {"message": "UpVote Successful"}


# Testing Route for Downvote
def test_downvote(authorize_client, test_create_posts):
    post_id = test_create_posts[2].id
    res = authorize_client.post("/vote", json={"post_id": post_id, "vote_dir": 0})

    assert res.status_code == 201
    assert res.json() == {"message": "DownVote Successful"}


# Testing Route for duplicate upvote
def test_duplicate_upvote(authorize_client, test_create_posts, test_existing_upvote):
    post_id = test_create_posts[3].id
    res = authorize_client.post("/vote", json={"post_id": post_id, "vote_dir": 1})

    assert res.status_code == 409


# Testing Route for duplicate downvote
def test_duplicate_downvote(authorize_client, test_create_posts, test_existing_downvote):
    post_id = test_create_posts[2].id
    res = authorize_client.post("/vote", json={"post_id": post_id, "vote_dir": 0})

    assert res.status_code == 409


# Testing Route for Unauthorised user upvote
def test_unauth_user_upvote(client, test_create_posts):
    post_id = test_create_posts[2].id
    res = client.post("/vote", json={"post_id": post_id, "vote_dir": 1})

    assert res.status_code == 401


# Testing Route for Unauthorised user downvote
def test_unauth_user_downvote(client, test_create_posts):
    post_id = test_create_posts[2].id
    res = client.post("/vote", json={"post_id": post_id, "vote_dir":0})

    assert res.status_code == 401


# Testing Route for Voting on Non-Existent Post
def test_vote_on_nonexistent_post(authorize_client):
    post_id = 9999
    res = authorize_client.post("/vote", json={"post_id": post_id, "vote_dir":1})

    assert res.status_code == 404


# Testing Route for Invalid Voting Dir.
def test_vote_on_nonexistent_post(authorize_client, test_create_posts):
    post_id = test_create_posts[2].id
    res = authorize_client.post("/vote", json={"post_id": post_id, "vote_dir":9999})

    assert res.status_code == 422

