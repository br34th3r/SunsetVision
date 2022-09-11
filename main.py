import json
import arrow
from SunsetVision import SunsetVision

# Request All Relevant Data
# - / Cloud Coverage Percentage
# - / Forecast (For rain and then a stop)
# - / Humidity Percentage
# - / Wind Speed and Changes

if __name__ == "__main__":
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
        data_file.close()

    ssv = SunsetVision(data)
    sunset_time = ssv.getSunsetTime()
    cloud_coverage_rating = ssv.rateCloudCoverage()
    air_quality_rating = ssv.rateAirQuality()
    change_in_wind_direction_rating = ssv.rateChangeInWindDirection()
    humidity_rating = ssv.rateHumidity()
    wind_speed_rating = ssv.rateWindSpeed()
    overall = sum([cloud_coverage_rating, air_quality_rating,
                   change_in_wind_direction_rating, humidity_rating, wind_speed_rating])

    print("Ratings for day %s sunset time:" % (sunset_time))
    print("Cloud Coverage: %s/4" % (cloud_coverage_rating))
    print("Air Quality: %s/4" % (air_quality_rating))
    print("Change in Wind Direction Rating: %s/4" %
          (change_in_wind_direction_rating))
    print("Humidity: %s/4" % (humidity_rating))
    print("Wind Speed: %s/4" % (wind_speed_rating))
    print("\nOverall Rating: %s/20" % (overall))

    goodSunset = ""
    match overall:
        case n if n == 20:
            goodSunset = "It should be fantastic"
        case n if n > 15:
            goodSunset = "Chances are high it should be nice"
        case n if n > 10:
            goodSunset = "It could be great, but no promises"
        case n if n > 5:
            goodSunset = "Not so sure about today, but miracles happen"
        case n if n >= 0:
            goodSunset = "Not a strong chance today, maybe you should hold off"
        case _:
            goodSunset = "Couldn't interpret the ratings for some reason, that's odd!"
    print(goodSunset)
