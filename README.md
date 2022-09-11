# SunsetVision

A python script to use the StormGlass API and the Sunrise-Sunset API to try and predict whether or not there will be a beautiful sunset in your area. Make sure to follow the instructions below carefully to get working!

## Usage

- Clone the repo using `git clone https://www.github.com/br34th3r/SunsetVision.git`
- Move into the new directory with `cd SunsetVision`
- Create a new text file called `api_key.txt` and add your StormGlass API key into it on one line
- Adjust the settings for your latitude and longitude in the `SunsetVision` class in the `SunsetVision.py` file
  - These are in the `__init__` method
- Currently this version pulls from a `data.txt` file supplied in the directory, to remedy this, utilise the `retrieveData` method in your class to make an API call and use the josn from that to define your `SunsetVision` class object, this is demoed in the example section below

## Example

```main.py
# This allows you to pull new data from the apis
from SunsetVision import SunsetVision

ssv = SunsetVision({})
data = ssv.retrieveData()
ssv.addData(data)
```
