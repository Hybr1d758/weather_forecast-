import requests
import pandas as pd
import matplotlib.pyplot as plt 
# program should ask user for these query parameters
# latitude, longitude
# user input validation -> sanity check

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_user_input():
    """
    This function asks user for latitude and longitude
    :returns latitude, longitude
    """
    try:
        latitude_input = float(input("Enter latitude: "))
        longitude_input = float(input("Enter longitude: "))
        return (latitude_input, longitude_input)
    except ValueError as error:
        print(f"Error: {error}")
        exit(1)

def get_url(latitude: float, longitude: float):
    """
    This function returns the url for the API call
    :param latitude: latitude of the location
    :param longitude: longitude of the location
    :returns url: url for the API call
    """
    required_params = "current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    url = f"{BASE_URL}?latitude={latitude}&longitude={longitude}&{required_params}"
    return url

def make_api_request(url: str):
    """
    This function makes the API call
    :param url: url for the API call
    :returns response_json: response from the API call
    """
    response = requests.get(url)
    status_code = response.status_code
    response_json = response.json()
    if status_code != 200:
        print(f"Error: API returned {status_code} code with mesage: {response_json}")
        exit(1)
    return response_json

def convert_response_to_csv(response_json: dict):
    """
    This function converts the response from the API call to csv format into a data.csv file
    :param response_json: response from the API call
    """
    

    hourly = response_json.get("hourly", [])
    time = hourly.get("time")
    temperature = hourly.get("temperature_2m")
    relative_humidity = hourly.get("relative_humidity_2m")
    wind_speed = hourly.get("wind_speed_10m")

    data = {
        "time": time,
        "temperature": temperature,
        "relative_humidity": relative_humidity,
        "wind_speed": wind_speed
    }

    df = pd.DataFrame(data)
    df.to_csv("forecast.csv", index=False)





def convert_csv_to_linear_graph():
    # read data from csv 
    df = pd.read_csv("forecast.csv")
    
    #plotting simple linear graph
    plt.plot(df["time"], df["temperature"], label='Temperature (°C)')
    plt.xlabel("time")
    plt.ylabel("Temperature")
    plt.title('Temperature Variation Over Time')
    plt.show()

# run the program
# 54.5742, 1.2350
if __name__ == "__main__":
    latitude, longitude = get_user_input()
    url = get_url(latitude, longitude)

    # make the API call
    response_json = make_api_request(url)
    
    # from response to csv
    convert_response_to_csv(response_json)

    # convert data into linear graph
    convert_csv_to_linear_graph()
