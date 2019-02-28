# aiohttp (see https://docs.aiohttp.org/en/stable/web_reference.html)
from aiohttp import web
import socketio
from pyparrot.Minidrone import Mambo

# create the app (aiohttp web server)
app = web.Application()

# create the socketio server and connect it to the http server
sio = socketio.AsyncServer()
sio.attach(app)

# pyparrot mambo vars
mamboAddr = "e0:14:d0:63:3d:d0"
mambo_ready = False

# route handler for index
async def get_index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# sio handler for message event
@sio.on('message')
async def connect(sid, msg):
    print('message from', sid)
    print('-->', msg)

# sio handler for connect event
@sio.on('connect')
async def connect(sid, env):
    print('connect ', sid)

# sio handler for disconnect event
@sio.on('disconnect')
async def disconnect(sid):
    print('disconnect ', sid)

# sio handler for takeoff event
@sio.on('takeoff')
async def takeoff(sid):
    print('sio takeoff command', sid)
    if (mambo_ready):
        mambo.safe_takeoff(5)

# sio handler for takeoff event
@sio.on('land')
async def land(sid):
    print('sio land command', sid)
    if (mambo_ready):
        mambo.safe_land(5)

# sio handler for turnright event
@sio.on('turnright')
async def turnright(sid):
    print('sio turnright command', sid)
    if (mambo_ready):
        mambo.turn_degrees(90)

# sio handler for turnleft event
@sio.on('turnleft')
async def turnleft(sid):
    print('sio turnleft command', sid)
    if (mambo_ready):
        mambo.turn_degrees(-90)

# register routes
app.router.add_get('/', get_index)

# pyparrot connection process (use ONLY on a Linux device ie:RaspberryPi with the appro)
mambo = Mambo(mamboAddr, use_wifi=False)
print("[M] Trying to connect to a Mambo drone over BLE...")
success = mambo.connect(num_retries=3)
print("[M] Connection to a Mambo drone: %s" % success)
if (success):
    mambo_ready = True
    print("[M] Mambo drone is READY")

# MAMBO commands (fyi)
    #mambo.smart_sleep(2)
    #mambo.ask_for_state_update()
    #mambo.sensors.flying_state ["emergency"]
    #mambo.safe_takeoff(5)
    #mambo.safe_land(5)
    #mambo.fly_direct(roll=0, pitch=50, yaw=0, vertical_movement=0, duration=1)
    #mambo.turn_degrees(90)
    #mambo.disconnect()
    #mambo.fire_gun()
    #success = mambo.flip(direction="left") ["left","right","front","back"]
    #mambo.hover()

# run the http server app
web.run_app(app, host='localhost', port=80, handle_signals=True)
