from pydantic import BaseModel

from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel, ImpressionModel


class Impression(BaseModel, orm_mode=True):
    """
    印象entity
    """

    main_character_id: int
    other_character_id: int
    impression: str

    @classmethod
    def _get_impression_about(cls, main_character_id: int, other_character_id: int):
        with (rdbms_instance.get_session() as session):
            filter_ = session.query(ImpressionModel)
            filter_ = filter_.filter(ImpressionModel.main_character_id == main_character_id)
            filter_.filter(ImpressionModel.other_character_id == other_character_id)
            results = filter_.all()
            return results

    @classmethod
    def get_impression_about(cls, main_character_id: int, other_character_id: int):
        results = cls._get_impression_about(main_character_id, other_character_id)
        if len(results) == 0:
            return None
        else:
            return cls.from_orm(results[0])

    @classmethod
    def renew_impression(cls, main_character_id: int, other_character_id: int, impression: str):
        with rdbms_instance.get_session() as session:
            results = cls._get_impression_about(main_character_id, other_character_id)

            if len(results) == 0:
                impression_model = ImpressionModel()
                impression_model.main_character_id = main_character_id
                impression_model.other_character_id = other_character_id
                impression_model.impression = impression
                session.add(impression_model)
            else:
                impression_model = results[0]
                impression_model.impression = impression
            session.commit()
