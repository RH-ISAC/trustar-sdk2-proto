
from base_class import Base

class Relation(Base):

    def __init__(self, entity, valid_from=None, valid_to=None, confidence=None):
        self.entity = entity
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.confidence_score = confidence