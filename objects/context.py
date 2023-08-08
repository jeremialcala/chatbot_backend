# -*- coding: utf8 -*-

class Context:
    sender_id: str
    context: str
    concepts: list
    user: dict

    def __init__(self, sentence, concepts, sender_id, user_data):
        self.sentence = sentence
        self.concepts = concepts
        self.sender_id = sender_id
        self.user = user_data
