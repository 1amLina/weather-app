import eel
import pyowm

owm = pyowm.OWM('your token')

@eel.expose
def get_weather(place):
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(place)
    w = observation.weather

    temp = w.temperature('celsius')['temp']
    # print("В городе " + place + " сейчас " + str(temp) + " градусов.")
    return "В городе " + place + " сейчас " + str(temp) + " градусов."

eel.init(r'D:\Python\work_practice\project2_weather_app\web')
eel.start('main.html', size=(700,700))
# # get_weather('Нью-Йорк, США')