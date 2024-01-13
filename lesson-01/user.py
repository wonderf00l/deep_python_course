
def fetch_vk_api(path, username, age):
    return ["q_50", "r_52", "c_53"]


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greetings(self):
        return f"Hello, {self.name}!"

    def birthday(self):
        self.age += 1
        return self.age

    def get_friends(self, age=None):
        friends = fetch_vk_api("/friends", self.name, age)

        if age is not None:
            friends = [fr for fr in friends if age in fr]

        return friends
