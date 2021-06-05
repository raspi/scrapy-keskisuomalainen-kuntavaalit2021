import scrapy

from kuntavaalit.items import *


class SiteSpider(scrapy.Spider):
    allowed_domains = [
        'vaalikone.media.fi',
    ]
    start_urls = [
        'https://vaalikone.media.fi/api/v1/public/elections/6/constituencies',
    ]

    def parse(self, response: scrapy.http.Response):
        raise NotImplemented

    def load_questions(self, response: scrapy.http.TextResponse):
        yield Question(
            url=response.url,
            data=response.json(),
        )

    def load_candidate_answers(self, response: scrapy.http.TextResponse):
        data = response.json()
        yield Answer(
            url=response.url,
            data=data,
            candidateid=data[0]['candidate_id'],
        )

    def load_candidates(self, response: scrapy.http.TextResponse):
        data = response.json()
        yield Candidate(
            url=response.url,
            data=data,
        )

        for i in data:
            yield scrapy.Request(
                response.urljoin(
                    f"https://vaalikone.media.fi/api/v1/public/elections/6/constituencies/{i['constituency_id']}/candidates/{i['id']}/answers"),
                callback=self.load_candidate_answers,
            )

    def load_parties(self, response: scrapy.http.TextResponse):
        yield Party(
            url=response.url,
            data=response.json(),
        )


class KuntaSpider(SiteSpider):
    """
    Fetch all from municipality X
    """

    name = 'kunta'
    id: str = ""

    def __init__(self, id: str = ""):
        if id == "":
            id = None

        if id is None:
            raise ValueError("no id")

        self.id = id

    def parse(self, response: scrapy.http.TextResponse):
        found: bool = False
        for i in response.json():
            if str(i['id']) == self.id:
                found = True
                break

        if not found:
            raise ValueError(f"id {self.id} not found")

        yield scrapy.Request(
            response.urljoin(f"https://vaalikone.media.fi/api/v1/public/elections/6/constituencies/{self.id}/parties"),
            callback=self.load_parties,
        )

        yield scrapy.Request(
            response.urljoin(
                f"https://vaalikone.media.fi/api/v1/public/elections/6/constituencies/{self.id}/questions"),
            callback=self.load_questions,
        )

        yield scrapy.Request(
            response.urljoin(
                f"https://vaalikone.media.fi/api/v1/public/elections/6/constituencies/{self.id}/candidates"),
            callback=self.load_candidates,
        )


class KVSpider(SiteSpider):
    """
    Fetch all
    """

    name = 'kaikki'

    def parse(self, response: scrapy.http.TextResponse):
        for i in response.json():
            yield scrapy.Request(
                response.urljoin(
                    f"https://vaalikone.media.fi/api/v1/public/elections/6/constituencies/{i['id']}/parties"),
                callback=self.load_parties,
            )

            yield scrapy.Request(
                response.urljoin(
                    f"https://vaalikone.media.fi/api/v1/public/elections/6/constituencies/{i['id']}/questions"),
                callback=self.load_questions,
            )

            yield scrapy.Request(
                response.urljoin(
                    f"https://vaalikone.media.fi/api/v1/public/elections/6/constituencies/{i['id']}/candidates"),
                callback=self.load_candidates,
            )
