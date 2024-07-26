

class Rule:

    def __init__(self, name):
        self.name = name

    def detect_misconfiguration(self, instance, *args, **kwargs) -> dict:
        pass

    def fix_misconfiguration(self,  instance, report, *args, **kwargs) -> dict:
        pass

    def get_name(self) -> str:
        return self.name