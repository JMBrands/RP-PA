from microdot import Microdot
import network
import time as t

app = Microdot()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ultramagic2', 'ultramagic.net')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    t.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
print("connected")
status = wlan.ifconfig()
print(status)
print("ip=",status[0])

htmldoc = '''<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
            <p><a href="/shutdown">Click to shutdown the server</a></p>
        </div>
    </body>
</html>
'''


@app.route('/')
def hello(request):
    print(request)
    return htmldoc, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


app.run(debug=True)