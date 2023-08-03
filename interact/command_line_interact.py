from pydantic import BaseModel


class CommandLineInteracter(BaseModel):
    class StopException(Exception):
        pass

    def next(self, prefix):
        ret = input(prefix).strip()
        if ret == "/stop":
            raise CommandLineInteracter.StopException("手动停止...")
        return ret
