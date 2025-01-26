from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    print(res.json())


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "asdasd"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "asdasdsad"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_posts(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "asdasdas"}
    )
    assert res.status_code == 401
