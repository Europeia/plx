from string import Template
from typing import Literal, Self, TypeIs, get_args

Chamber = Literal["ga", "sc"]
Position = Literal["for", "against", "abstain", "no recommendation"]


def is_chamber(value: str) -> TypeIs[Chamber]:
    return value in get_args(Chamber)


def is_position(value: str) -> TypeIs[Position]:
    return value in get_args(Position)


RECOMMENDATION_COLORS: dict[Position, str] = {
    "for": "green",
    "against": "red",
    "abstain": "yellow",
    "no recommendation": "yellow",
}

CHAMBER_TITLE: dict[Chamber, str] = {
    "ga": "General Assembly",
    "sc": "Security Council",
}


class Dispatch:
    def __init__(self, template: Template):
        self._template = template

    @classmethod
    def from_file(cls, file_path: str) -> Self:
        with open(file_path, "r") as f:
            template = Template(f.read())

        dispatch = cls(template)

        return dispatch

    def format(
        self,
        proposal_name: str,
        chamber: Chamber,
        forum_thread_url: str,
        position: Position,
        proposal_overview: str,
        ministry_analysis: str,
        ifv_author: str,
        mowaa_nation: str,
        mowaa_forum: str,
        europeia_del: str,
        estalcia_del: str,
    ) -> str:
        return self._template.substitute(
            proposal_name=proposal_name,
            chamber=chamber,
            forum_thread_url=forum_thread_url,
            recommendation_color=RECOMMENDATION_COLORS[position],
            position=position.upper(),
            proposal_overview=proposal_overview,
            ministry_analysis=ministry_analysis,
            ifv_author=ifv_author,
            mowaa_nation=mowaa_nation,
            mowaa_forum=mowaa_forum,
            europeia_del=europeia_del,
            estalcia_del=estalcia_del,
        )


class Telegram:
    def __init__(self, template: Template):
        self._template = template

    @classmethod
    def from_file(cls, file_path: str) -> Self:
        with open(file_path, "r") as f:
            template = Template(f.read())

            telegram = cls(template)

            return telegram

    def format(
        self,
        chamber: Chamber,
        proposal_name: str,
        forum_thread_url: str,
        position: Position,
        ifv_dispatch_url: str,
        mowaa_nation: str,
        mowaa_forum: str,
        europeia_del: str,
        estalcia_del: str,
    ) -> str:
        return self._template.substitute(
            chamber_title=CHAMBER_TITLE[chamber],
            chamber=chamber,
            proposal_name=proposal_name,
            forum_thread_url=forum_thread_url,
            position=position.upper(),
            ifv_dispatch_url=ifv_dispatch_url,
            mowaa_nation=mowaa_nation,
            mowaa_forum=mowaa_forum,
            europeia_del=europeia_del,
            estalcia_del=estalcia_del,
        )
