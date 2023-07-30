from typing import Union

from langchain.tools import BaseTool
from pydantic import BaseModel
import requests
import logging


class WeatherInfo(BaseModel):
    country: str
    city: str
    wind: str
    wind_speed: str
    air_level: str
    temperature_now: str
    temperature_highest: str
    temperature_lowest: str


class GetWeatherInformationInChina(BaseTool):
    name = "get_weather_information_in_china"
    description = ("useful for when you need to get the current weather information only in China"
                   "firstly, you must know which country is the location of, "
                   "if it's china call this tool, "
                   "but if it isn't, do not call."
                   "secondly, you must make sure the location is a valid city.")

    @staticmethod
    def get_weather(location: str) -> Union[WeatherInfo, str]:
        try:
            logging.info(f"location of the request is {location}")
            resp = requests.get(
                f'http://www.tianqiapi.com/api?version=v6&appid=23035354&appsecret=8YvlPNrz&city={location}')
            resp.encoding = 'utf-8'
            content = resp.json()

            wi = WeatherInfo(
                city=content['city'],
                country=content['country'],
                wind=content['win'],
                wind_speed=content['win_speed'],
                air_level=content['air_level'],
                temperature_now=content['tem'],
                temperature_lowest=content['tem2'],
                temperature_highest=content['tem1'])

            logging.info(f"response {wi}")
            return wi
        except Exception as e:
            logging.error(e)
            return "get_weather failed because of bad network, maybe tell the user to shutoff the proxy will be better"

    def _run(self, location: str) -> WeatherInfo:
        return self.get_weather(location)

    async def _arun(self, location: str) -> WeatherInfo:
        return self.get_weather(location)
