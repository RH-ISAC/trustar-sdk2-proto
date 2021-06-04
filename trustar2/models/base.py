class Base(object):

    TYPE_ATTRIBUTES = ("_entity_type", "workflow_type")

    @staticmethod
    def _get_camelcase(attribute):
        if attribute in Base.TYPE_ATTRIBUTES:
            return "type"

        tmp = attribute.split("_")
        return tmp[0] + "".join([w.title() for w in tmp[1:]])

    @staticmethod
    def _get_serialized(attribute_value):
        serializable = getattr(attribute_value, "serialize", None)
        if serializable:
            attribute_value = attribute_value.serialize()

        return attribute_value

    def _get_serialized_attribute(self, attribute_value):
        if isinstance(attribute_value, list):
            attribute_value = [self._get_serialized(a) for a in attribute_value]

        else:
            attribute_value = self._get_serialized(attribute_value)

        return attribute_value

    def serialize(self):
        return {self._get_camelcase(k): self._get_serialized_attribute(v)
                for k, v in self.__dict__.items()
                if v is not None
                }


class Entity(Base):

    def __init__(self, value):
        self.value = value
