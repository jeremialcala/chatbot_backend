import json


class Product:
    def __init__(self, _id=None, title=None, tags: list = None, store=None, price=None, options: list = None,
                 image_url=None, subtitle=None, buttons: list = None):
        super().__init__()
        self._id = _id
        self.title = title
        self.tags = tags
        self.store = store
        self.price = price
        self.options = options
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = buttons

    def get_element(self):
        return json.dumps({"title": self.title, "image_url": self.image_url,
                           "subtitle": self.subtitle, "buttons": self.buttons})