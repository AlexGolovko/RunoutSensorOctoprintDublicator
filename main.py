import uasyncio
import ujson as json
import machine

from lib.microdot_asyncio import Microdot

# if __name__ == '__main__':
app = Microdot()


@app.get('/home')
async def hello(request):
    return 'Hello, world!'


@app.post('/pwd')
async def save_wifi_pwd(request):
    request_body = request.json
    print(str(request_body))
    ssid = request_body.get('ssid')
    pwd = request_body.get('pwd')
    with open("config.json", "w") as f:
        f.write(json.dumps({"ssid": ssid, "pwd": pwd}))
        f.flush()


def check():
    print('check')
    return -1


async def runout_sensor_checker():
    while True:
        await uasyncio.sleep(30)
        check()


print('run')
uasyncio.create_task(runout_sensor_checker())
app.run()
# sudo cu -s 115200 -l /dev/tty.usbmodem1401
