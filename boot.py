# This file is executed on every boot (including wake-boot from deepsleep)
import utime
import esp
import gc
import machine
import network
import ujson as json

esp.osdebug(None)

machine.freq(80000000)


def do_create_apif():
    ssid = 'runoutSensorDublicator'
    password = 'admin'
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)
    while not ap_if.active():
        pass
    print('Access Point created')
    print(ap_if.ifconfig())


def do_connect(wifi_name, wifi_pass):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    utime.sleep_ms(200)
    if wifi_name in str(wlan.scan()):
        print('connecting to network...')
        wlan.connect(wifi_name, wifi_pass)
        while not wlan.isconnected():
            pass
        print('network config:', wlan.ifconfig())
        print('wifi connected')
        return True
    else:
        wlan.active(False)
        return False


try:
    with open("config.json", "r") as f:
        config = f.read()
    if config:
        config = json.loads(config)
        wifi_name = config.get('ssid')
        wifi_pass = config.get('pwd')
        if not do_connect(wifi_name, wifi_pass):
            do_create_apif()
    else:
        do_create_apif()
except Exception as e:
    print(str(e))
    do_create_apif()
gc.collect()
print('boot finished')
