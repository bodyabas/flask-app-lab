import json

URL_JSON = 'app/posts/posts.json'

def load_posts() -> list[dict]:
    try:
        with open(file=URL_JSON, mode='r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    

def save_post(post: dict):
    posts = load_posts()
    posts.append(post)
    with open(file=URL_JSON, mode="w") as file:
        json.dump(posts, file, indent=4)

def get_post(id: int):
    posts = load_posts()
    if id > len(posts) or id < 1:
        return None
    post = next(post for post in posts if post["id"] == id)
    return post