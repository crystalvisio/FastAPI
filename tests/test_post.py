# Testing Route for Getting All Posts
def test_get_all_posts(authorize_client, test_create_posts):
    res = authorize_client.get("/post")

    print(res.json())

    assert res.status_code == 200
    assert len(res.json()) == len(test_create_posts)