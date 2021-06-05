from dataclasses import dataclass


@dataclass
class Item:
    url: str
    data: dict


@dataclass
class Candidate(Item):
    pass


@dataclass
class Party(Item):
    pass


@dataclass
class Question(Item):
    pass


@dataclass
class Answer(Item):
    candidateid: int
