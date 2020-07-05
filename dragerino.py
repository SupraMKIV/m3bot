from linemk4 import LineClient
import time, random, livejson, threading, urllib2, traceback
db = livejson.File("all.json", pretty=True)
### LOGIN ###
def qrlogin():
    print 'No valid token, QR Login? (Y/N)'
    do_qr = raw_input()
    if do_qr is 'Y':
        print 'You have 2 minutes to QR'
        client = LineClient('a', 'b')
        del do_qr
        return client
    else: exit()

def registerUser(uid, group, name):
    firstcar = random.choice("Golf4", "Tiburon", "Tigra")
    db["usr"][uid] = {
        "name": str(name),
        "bal": 3500,
        "cmdc": 0,
        "wins": 0,
        "lvl": 1,
        "xp": 0,
        "ai": 0,
        "car": [firstcar, 0, 0, 0, ""]
    }
    group.sendMessage(name+": Congrats! You have been awarded $3500 and you received a "+firstcar+" as your first automobile.")

if db['authToken']:
    print 'Logging in via token...'
    try: client = LineClient(authToken=db['authToken'])
    except: client = qrlogin()
else: client = qrlogin()

db['authToken'] = client.authToken
client.refreshGroups()
client.refreshContacts()


while 1:
    try:
### POLL ###
        for op in client._fetchOperations(client.revision, 50):
            client.revision = max(op.revision, client.revision)
            if op.type == 26 and op.message.text:
                rcvr = client.getGroupById(op.message.to)
                if not rcvr: break
                txt = op.message.text[1:] if op.message.text[0] is '!' else ""
                if not txt or len(txt) > 60: break
### COMMANDS ###
                if txt is "ping": rcvr.sendMessage("pong")
                elif txt is "sticker": rcvr.sendImageWithURL('https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/' + str(random.randint(2000, 9997695)) + '/android/sticker.png;compress=true')
                elif txt in ("shop", "tune", "swap", "drag", "lotto", "garage", "gta", "stats"):
                    if op.message.from.id in db["usr"]:
                        pass
                    else: rcvr.sendMessage(str(op.message.from.name)+": Please register first using !register")
                elif txt is "register":
                    if op.message.from.id in db["usr"]: rcvr.sendMessage(str(op.message.from.name)+": very funny, you dummy")
                    else: registerUser(op.message.from.id, rcvr, op.message.from.name) 
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()