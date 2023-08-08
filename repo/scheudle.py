from typing import Optional

from pydantic import BaseModel

from datasource.config import rdbms_instance
from datasource.rdbms.entities import ScheduleModel, ScheduleLogModel

SCHEDULE_COUNT = 8


class Schedule(BaseModel, orm_mode=True):
    character_id: int
    items_to_do: list[str]
    item_doing: Optional[str]

    def apply_item(self):
        self.item_doing = self.items_to_do[0]
        self.items_to_do = self.items_to_do[1:]

    def need_to_schedule(self):
        return len(self.items_to_do) == 0

    @classmethod
    def get_recent_done_items(cls, character_id, limit=10):
        with (rdbms_instance.get_session() as session):
            recent_done_items = session.query(
                ScheduleLogModel
            ).filter(ScheduleLogModel.character_id == character_id
                     ).order_by(ScheduleLogModel.create_time.asc()
                                ).limit(limit).all()
            return [_.item_done for _ in recent_done_items]

    def finish_item(self, item_done, item_doing, items_to_do):
        with (rdbms_instance.get_session() as session):
            # 记录schedule log
            log = ScheduleLogModel()
            log.character_id = self.character_id
            log.item_done = item_done
            session.add(log)

            # 调整计划
            self.item_doing = item_doing
            self.items_to_do = items_to_do
            self._renew(session, self)
            session.commit()

    @classmethod
    def _renew(cls, session, schedule):
        schedule: cls
        ret = session.query(ScheduleModel
                            ).filter(ScheduleModel.character_id == schedule.character_id
                                     ).all()

        if len(ret) == 0:
            schedule_orm = ScheduleModel()
            schedule_orm.character_id = schedule.character_id
            schedule_orm.items_to_do = schedule.items_to_do
            schedule_orm.item_doing = schedule.item_doing
            session.add(schedule_orm)
        else:
            schedule_orm = ret[0]
            schedule_orm.items_to_do = schedule.items_to_do
            schedule_orm.item_doing = schedule.item_doing

    @classmethod
    def renew(cls, schedule):
        with (rdbms_instance.get_session() as session):
            cls._renew(session, schedule)
            session.commit()

    @classmethod
    def get_by_character(cls, character_id: int):
        with (rdbms_instance.get_session() as session):
            ret = session.query(ScheduleModel
                                ).filter(ScheduleModel.character_id == character_id
                                         ).all()
            if len(ret) == 0:
                return None
            else:
                return cls.from_orm(ret[0])
