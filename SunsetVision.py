import arrow
import requests


class SunsetVision:
    def __init__(self, data):
        self.data = {}
        self.lat = 52.651740
        self.lng = 0.104020
        self.addData(data)

    def retrieveData(self):
        start = arrow.now().floor('day').shift(days=-3)
        end = arrow.now().ceil('day').shift(days=+3)
        params = ['cloudCover', 'humidity', 'visibility',
                  'windSpeed100m', 'windDirection100m', 'precipitation']

        with open("api_key.txt", "r") as key_file:
            api_key = key_file.readline().strip()
            key_file.close()

        response = requests.get(
            "https://api.stormglass.io/v2/weather/point",
            params={
                'lat': self.lat,
                'lng': self.lng,
                'start': start.to('UTC').timestamp(),
                'end': end.to('UTC').timestamp(),
                'params': ','.join(params)
            },
            headers={
                'Authorization': api_key
            }
        )

        return response.json()

    def addData(self, data):
        for hour in data["hours"]:
            date_and_time = arrow.get(hour["time"])
            if date_and_time.date() in self.data:
                self.data[date_and_time.date()].append(hour)
            else:
                self.data[date_and_time.date()] = [hour]

    def getSunsetTime(self, chosen_date=arrow.now()):
        response = requests.get("https://api.sunrise-sunset.org/json?lat=%s&lng=%s&date=%s" %
                                (self.lat, self.lng, chosen_date.format("YYYY-MM-DD")))
        return arrow.get(chosen_date.format("YYYY-MM-DD") + " " + response.json()["results"]["sunset"], "YYYY-MM-DD h:mm:ss A")

    def getCloudCoverageAtSunset(self, chosen_date):
        sunset = self.getSunsetTime(chosen_date)
        closest = None
        coverage = 0
        for hour in self.data[chosen_date.date()]:
            difference = abs(arrow.get(hour["time"]) - sunset)
            if closest == None:
                closest = difference
                coverage = (hour["cloudCover"]["dwd"] + hour["cloudCover"]
                            ["noaa"] + hour["cloudCover"]["sg"]) / 3
                continue
            if difference < closest:
                closest = difference
                coverage = (hour["cloudCover"]["dwd"] + hour["cloudCover"]
                            ["noaa"] + hour["cloudCover"]["sg"]) / 3
        return coverage

    def getDailyAveragePrecipitation(self, chosen_date):
        avg = 0
        for hour in self.data[chosen_date.date()]:
            avg += (hour["precipitation"]["dwd"] + hour["precipitation"]
                    ["noaa"] + hour["precipitation"]["sg"]) / 3
        return avg / len(self.data[chosen_date.date()])

    def getPrecipitationAtSunset(self, chosen_date):
        sunset = self.getSunsetTime(chosen_date)
        closest = None
        precipitation = 0
        for hour in self.data[chosen_date.date()]:
            difference = abs(arrow.get(hour["time"]) - sunset)
            if closest == None:
                closest = difference
                precipitation = (hour["precipitation"]["dwd"] +
                                 hour["precipitation"]["noaa"] +
                                 hour["precipitation"]["sg"]) / 2
                continue
            if difference < closest:
                closest = difference
                precipitation = (hour["precipitation"]["dwd"] +
                                 hour["precipitation"]["noaa"] +
                                 hour["precipitation"]["sg"]) / 2
        return precipitation

    def getHumidityAtSunset(self, chosen_date):
        sunset = self.getSunsetTime(chosen_date)
        closest = None
        humidity = 0
        for hour in self.data[chosen_date.date()]:
            difference = abs(arrow.get(hour["time"]) - sunset)
            if closest == None:
                closest = difference
                humidity = (hour["humidity"]["dwd"] + hour["humidity"]
                            ["noaa"] + hour["humidity"]["sg"]) / 3
                continue
            if difference < closest:
                closest = difference
                humidity = (hour["humidity"]["dwd"] + hour["humidity"]
                            ["noaa"] + hour["humidity"]["sg"]) / 3
        return humidity

    def getDailyAverageWindDirection(self, chosen_date):
        avg = 0
        for hour in self.data[chosen_date.date()]:
            avg += (hour["windDirection100m"]["noaa"] +
                    hour["windDirection100m"]["sg"]) / 2
        return avg / len(self.data[chosen_date.date()])

    def getWindDirectionAtSunset(self, chosen_date):
        sunset = self.getSunsetTime(chosen_date)
        closest = None
        windDirection = 0
        for hour in self.data[chosen_date.date()]:
            difference = abs(arrow.get(hour["time"]) - sunset)
            if closest == None:
                closest = difference
                windDirection = (
                    hour["windDirection100m"]["noaa"] + hour["windDirection100m"]["sg"]) / 2
                continue
            if difference < closest:
                closest = difference
                windDirection = (
                    hour["windDirection100m"]["noaa"] + hour["windDirection100m"]["sg"]) / 2
        return windDirection

    def getDailyAverageWindSpeed(self, chosen_date):
        avg = 0
        for hour in self.data[chosen_date.date()]:
            avg += (hour["windSpeed100m"]["noaa"] +
                    hour["windSpeed100m"]["sg"]) / 2
        return avg / len(self.data[chosen_date.date()])

    def rateCloudCoverage(self, chosen_date=arrow.now()):
        percentageAtSunset = float(self.getCloudCoverageAtSunset(chosen_date))
        match percentageAtSunset:
            case n if n < 30 or n > 70:
                return 0
            case n if n < 35 or n > 65:
                return 1
            case n if n < 40 or n > 60:
                return 2
            case n if n < 45 or n > 55:
                return 3
            case n if n > 45 and n < 55:
                return 4
            case _:
                return 0

    def rateAirQuality(self, chosen_date=arrow.now()):
        dailyAveragePrecipitation = self.getDailyAveragePrecipitation(
            chosen_date)
        precipitationAtSunset = self.getPrecipitationAtSunset(chosen_date)

        if precipitationAtSunset > dailyAveragePrecipitation:
            return 0

        match dailyAveragePrecipitation - precipitationAtSunset:
            case n if n < 10:
                return 1
            case n if n < 40:
                return 2
            case n if n < 70:
                return 3
            case n if n > 70:
                return 4
            case _:
                return 0

    def rateHumidity(self, chosen_date=arrow.now()):
        humidityAtSunset = self.getHumidityAtSunset(chosen_date)
        match humidityAtSunset:
            case n if n > 90:
                return 0
            case n if n > 70:
                return 1
            case n if n > 50:
                return 2
            case n if n > 30:
                return 3
            case n if n > 10:
                return 4
            case _:
                return 0

    def rateChangeInWindDirection(self, chosen_date=arrow.now()):
        dailyAverageWindDirection = self.getDailyAverageWindDirection(
            chosen_date)
        windDirectionAtSunset = self.getWindDirectionAtSunset(chosen_date)
        match abs(dailyAverageWindDirection - windDirectionAtSunset):
            case n if n < 20:
                return 0
            case n if n < 50:
                return 1
            case n if n < 90:
                return 2
            case n if n < 120:
                return 3
            case n if n > 120:
                return 4
            case _:
                return 0

    def rateWindSpeed(self, chosen_date=arrow.now()):
        dailyAverageWindSpeed = self.getDailyAverageWindSpeed(chosen_date)
        match dailyAverageWindSpeed:
            case n if n > 13:
                return 0
            case n if n > 9:
                return 1
            case n if n > 6:
                return 2
            case n if n > 4:
                return 3
            case n if n > 2:
                return 4
            case _:
                return 0
