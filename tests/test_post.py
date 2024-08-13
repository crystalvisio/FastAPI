from app import schemas


demo_post_data = {
    "title": "Demo Post Title",
    "content": "This is a demo post for testing"
}

update_data = {
    "title": "Updated Post Title",
    "content": "Updated Post Content",
    "published": False  # Explicitly changing the published status
}


# Testing Route for Getting All Posts
def test_get_all_posts(authorize_client, test_create_posts):
    res = authorize_client.get("/post")

    posts = [schemas.PostOut(**post).model_dump() for post in res.json()]

    for post in posts:
        print(post)

    assert res.status_code == 200
    assert len(res.json()) == len(test_create_posts)


# Testing Route For Unauthorized User Getting All Posts
def test_unauthorized_user_get_all_posts(client, test_create_posts):
    res = client.get("/post")

    print(res.json())

    assert res.status_code == 401


# Testing Route For Unauthorized User Getting One Posts
def test_unauthorized_user_get_one_post(client, test_create_posts):
    post_id = test_create_posts[0].id
    res = client.get(f"/post/{post_id}")

    print(res.json())

    assert res.status_code == 401


# Testing Route for Post Not Found
def test_post_not_found(authorize_client, test_create_posts):
    res = authorize_client.get(f"/post/8888888")
    
    assert res.status_code == 404


# Testing Route For Creating a Post
def test_auth_user_create_post(authorize_client):
    res = authorize_client.post("/post", json = demo_post_data)
    
    print(res.json())

    new_post = schemas.PostCreate(**res.json())

    assert res.status_code == 201
    assert new_post.title == "Demo Post Title"
    assert new_post.published == True # Published should default to True if not provided


# Testing Route For Unauthorized user creating post
def test_unautorize_user_create_post(client):
    res = client.post("/post", json = demo_post_data)

    assert res.status_code == 401


# Testing Route for Updating a Post
def test_update_post(authorize_client, test_create_posts):
    post_id = test_create_posts[0].id

    res = authorize_client.put(f"/post/{post_id}", json = update_data)
    
    print(res.json())

    assert res.status_code == 200

    updated_post = schemas.PostBase(**res.json())

    assert updated_post.title == "Updated Post Title"
    assert updated_post.published == False


# Testing Route For Unauthorized user updating post
def test_unauth_user_update_post(client, test_create_posts):
    post_id = test_create_posts[0].id
    res = client.put(f"/post/{post_id}", json = update_data)

    assert res.status_code == 401


# Testing Route for Deleting a Post
def test_del_post(authorize_client, test_create_posts):
    post_id = test_create_posts[0].id
    res = authorize_client.delete(f"/post/{post_id}")

    assert res.status_code == 204


# Testing Route For Unauthorized user deleting post
def test_unauth_user_del_post(client, test_create_posts):
    post_id = test_create_posts[0].id
    res = client.delete(f"/post/{post_id}")

    assert res.status_code == 401

    