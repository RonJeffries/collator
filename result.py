from dataclasses import dataclass

@dataclass
class Result:
    name: str
    outcome: str
    is_new: bool