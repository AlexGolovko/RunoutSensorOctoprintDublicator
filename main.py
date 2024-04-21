import uasyncio
import ujson as json
import machine
import urequests
from lib.microdot_asyncio import Microdot

CONFIG_FILENAME = "config.json"
CONFIG = {}
app = Microdot()

try:
    with open(CONFIG_FILENAME, "r") as f:
        CONFIG = json.loads(f.read())
except Exception as e:
    print("Error reading config file:", e)


@app.get('/home')
async def home(request):
    with open("/static/home.html", "r") as f:
        response_body = f.read()
        f.close()
        return response_body, 200, {'Content-Type': 'text/html'}


@app.post('/config')
async def save_wifi_pwd(request):
    with open(CONFIG_FILENAME, "w") as f:
        f.write(json.dumps(request.json))
        f.flush()


runout_sensor_pin = machine.Pin(2, machine.Pin.IN)  # GPIO2


def check():
    if runout_sensor_pin.value() == 1:
        host = CONFIG.get('octoprint_host')
        port = CONFIG.get('octoprint_port')
        url = "http:" + host + ":" + port + "/api/job"
        api_key = CONFIG.get("octoprint_api_key")
        data = {
            "command": "pause",
            "action": "pause"
        }
        headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        response = urequests.post(url, headers=headers, json=data)
        if response.status_code < 300:
            print("Job paused successfully!")
        else:
            print("Error pausing job:", response.status_code)
        response.close()


async def runout_sensor_checker():
    while True:
        await uasyncio.sleep(30)
        try:
            check()
        except Exception as e:
            print(str(e))


print('run')
uasyncio.create_task(runout_sensor_checker())
app.run()
# sudo cu -s 115200 -l /dev/tty.usbmodem1401
