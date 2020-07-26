from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    IntField,
    DateTimeField,
    EmbeddedDocumentField,
)


class AdditionalDetails(EmbeddedDocument):
    pass


class Association(EmbeddedDocument):
    id = IntField()
    login = StringField()
    name = StringField()
    type = StringField()

    meta = {"allow_inheritance": True}


class Source(Association):
    pass


class CreatedBy(Association):
    pass


class BoxEvent(Document):
    additional_details = EmbeddedDocumentField(AdditionalDetails)
    created_by = EmbeddedDocumentField(CreatedBy)
    source = EmbeddedDocumentField(Source)
    event_id = StringField()
    event_type = StringField()
    session_id = StringField()
    type = StringField()
    created_at = DateTimeField()

    @classmethod
    def insert_box_event_from_dict(cls, event_dict):
        event = cls(
            additional_details=AdditionalDetails(),
            created_by=CreatedBy(
                id=event_dict["created_by"]["id"],
                login=event_dict["created_by"]["login"],
                name=event_dict["created_by"]["name"],
                type=event_dict["created_by"]["type"],
            ),
            source=Source(
                id=event_dict["source"]["id"],
                login=event_dict["source"]["login"],
                name=event_dict["source"]["name"],
                type=event_dict["source"]["type"],
            ),
            event_id=event_dict["event_id"],
            event_type=event_dict["event_type"],
            session_id=event_dict["session_id"],
            type=event_dict["type"],
            created_at=event_dict["created_at"],
        )
        event.save()

        return event
