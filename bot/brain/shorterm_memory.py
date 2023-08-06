from bot.message import Message
from repo.character import Character
from repo.history import History, Direction


class ShortTermMemory:
    def __init__(self, character: Character, max_length: int):
        self.character = character
        self.max_length = max_length

    def add(self, character_input: Character, message_in: Message, message_out: Message):
        History.add(History(main_character=self.character,
                            other_character=character_input,
                            main_message=message_out.message,
                            main_action=message_out.action,
                            other_message=message_in.message,
                            other_action=message_in.action,
                            direction=Direction.to_main
                            ))

    def shrink(self):
        history_list = History.get_available_history_by_character_id(self.character.id)
        if len(history_list) >= self.max_length:
            shrink_cnt = int(len(history_list) / 2)
            ret_list = history_list[0: shrink_cnt]

            return ret_list
        return []

    @classmethod
    def batch_set_history_remembered(cls, ids: list[int]):
        History.batch_set_history_remembered(ids)

    def to_prompt(self):
        history_list = History.get_available_history_by_character_id(self.character.id)
        ret = ""
        for history in history_list:
            dialog = str(history)

            ret += dialog
        if len(ret) == 0:
            return "没有数据"
        return ret

# class ShortTermMemory(BaseMemory):
#     class BaseLimiter:
#         @abstractmethod
#         def limit(self, statement):
#             pass
#
#     class LengthLimiter(BaseLimiter):
#
#         def __init__(self, cnt: int):
#             self.cnt = cnt
#
#         def limit(self, statement):
#             return statement.limit(self.cnt).all()
#
#     character1_id: int
#     character2_id: int
#     limiter: BaseLimiter
#
#     def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
#         with rdbms_instance.get_session() as session:
#             history = HistoryModel()
#             history.character1_id = self.character1_id
#             history.character2_id = self.character2_id
#             history.character1_message = inputs["input"]
#             history.character2_message = outputs["output"]
#             session.add(history)
#             session.commit()
#
#     @property
#     def memory_variables(self) -> List[str]:
#         return ["history"]
#
#     def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
#         """Retrieve all messages from db"""
#         with rdbms_instance.get_session() as session:
#             statement = session.query(HistoryModel).filter(
#                 HistoryModel.character1_id == self.character1_id
#                 and HistoryModel.character2_id == self.character2_id
#             )
#             results = self.limiter.limit(statement)
#             messages = []
#             for record in results:
#                 record: HistoryModel
#                 message = History.from_orm(record)
#                 messages.append(message)
#             return {"history": messages}
#
#     def clear(self) -> None:
#         pass
