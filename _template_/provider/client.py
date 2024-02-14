from flask import current_app as app

client = None


class ExampleAPIClient:
    def __init__(self, example):
        # Define any class parameters here. If they are absolutely necessary for the client
        # to function, they should be asserted when being retrieved in the external get_client() method
        self.example = example

    def search(self, query):
        data = [
            {
                "id": "1",
                "title": "Tall penguins",
                "text": "The tallest penguin is the Emperor penguin",
                "url": "https://en.wikipedia.org/wiki/Penguin",
            },
            {
                "id": "2",
                "title": "Emperor penguins",
                "text": "The latin name for Emperor penguin is Aptenodytes forsteri",
                "url": "https://en.wikipedia.org/wiki/Penguin",
            },
            {
                "id": "3",
                "title": "Small penguins",
                "text": "The smallest penguin is the fairy penguin",
                "url": "https://en.wikipedia.org/wiki/Penguin",
            },
            {
                "id": "4",
                "title": "Eudyptula penguis",
                "text": "The latin name for fairy penguin is Eudyptula minor",
                "url": "https://en.wikipedia.org/wiki/Penguin",
            },
        ]

        return data


def get_client():
    # Use the global client if your client hasn't implemented OAuth
    global client
    if client is None:
        # Here you can fetch environment variables with the Flask app configs
        # If this needed to be asserted, you could use:
        # assert (example := app.config.get("EXAMPLE_ENV_VAR")), "TEMPLATE_EXAMPLE_ENV_VAR must be set"
        example = app.config.get("EXAMPLE_ENV_VAR", "")

        client = ExampleAPIClient(example)

    return client
