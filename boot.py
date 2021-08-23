import os 
import time
import socket 

import network
import machine
import ssd1306

from machine import Pin, I2C 


CONF="http.conf"
SSID="GOODJOB"
PASSWD="12345678"
RESETPIN=13

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)


def display(text):
    try:
        i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000);
        display = ssd1306.SSD1306_I2C(128, 64, i2c)
        display.text(text, 0, 0, 1)
        display.show()
    except:
        pass
    print("%s"%text)
def start_sta(): 
    adminpass=""
    try:
        with open(CONF,"r") as f:
            sta_if.active(True)
            ap_if.active(False)
            ssid=f.readline().strip()
            passwd=f.readline().strip()
            adminpass=f.readline().strip()
            sta_if.connect(ssid, passwd)
            display("to %s"%ssid)
    except:
        sta_if.active(False)
        ap_if.active(True)
        ap_if.ifconfig(("192.168.1.1","255.255.255.0","192.168.1.1","192.168.1.1"))
        ap_if.config(essid=SSID,password=PASSWD)
        display("SSID:%s passwd:%s ip:%s"%(SSID,PASSWD,ap_if.ifconfig()[0]))
    return adminpass

def callback(g):
    display("reset conf ..")
    try:
        import os;os.remove(CONF)
    except:
        pass
    machine.reset()

print("\n=============")
rstpin = machine.Pin(RESETPIN,mode=machine.Pin.IN)
rstpin.value(1) # default up on start up
rstpin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)    

adminpass=start_sta()   
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
while True:
    ip = sta_if.ifconfig()[0] if sta_if.active() else ap_if.ifconfig()[0]
    display("IP:%s"%(ip))
    
    if "0.0.0.0" == ip:
        time.sleep(1)
        continue
    
    cl, addr = s.accept()
    cl_file = cl.makefile('rw', 0)

    
    while True:
        l = cl_file.readline()
        if "GET" in l:
            line = l.decode()
        if not l or l == b'\r\n':
            break
    response = '''
    Pull D7(GPIO%d) down to reset<br/> 
    <form action=''>
    <input name='ssid' placeholder='ssid'/>
    <input name='passwd' type='password' placeholder='passwd'/>
    <input name='adminpass' type='password' placeholder='adminpass'/>
    <input type='submit' value='ok'/>
    </form>
    '''%(RESETPIN)
    statucode="HTTP/1.0 200 OK"
    if "?" in line:
        params=dict([tuple(p.split("=")) for p in line.split("?")[1].split(" ")[0].split("&")])
        if "adminpass" not in params: params["adminpass"]=""
        if adminpass == "" or adminpass == params["adminpass"].strip():
            if "ssid" in params:
                with open(CONF,"w") as f:
                    f.write(params["ssid"]+"\n")
                    f.write(params["passwd"]+"\n")
                    f.write(params["adminpass"]+"\n")
                response="ok"
                adminpass=start_sta() 
            elif "pin" in params:
                gpio=int(params["pin"])
                pin = machine.Pin(gpio, machine.Pin.OUT)
                if "value" in params:  
                    if params["value"]=="toggle":
                        pin.value(not pin.value())
                    elif params["value"]=="1":
                        pin.value(1)
                    elif params["value"]=="0":
                        pin.value(0)
                response="gpio%s=%s"%(gpio,pin.value())
        else:
            statucode="HTTP/1.0 403 Forbidden"
            response="Forbidden"
        display(response)
    cl.send('%s\r\nContent-type: text/html\r\n\r\n%s\r\n'%(statucode,response))
    cl.close()
    
