# ESP8266 http switch with web interface micropython implement



### how to use
* flash micropython fireware,[guidance](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html) to micropython official site 
* upload boot.py to board 

> * Getting a MicroPython REPL prompt [guidance](https://docs.micropython.org/en/latest/esp8266/tutorial/repl.html)
> * enable WebREPL [guidance](https://docs.micropython.org/en/latest/esp8266/quickref.html#webrepl-web-browser-interactive-prompt) 
> * setup webrepl 

>> * `import webrepl_setup`

>> * input E
  
>> * input your password eg.123456 and repeat your password
   
>> * `input y to reboot the device`
      
>> * enable webrepl  `import webrepl;webrepl.start()   `
     
>> * in host `{path to webrepl_cli.py}/webrepl_cli.py -p 123456 boot.py 192.168.4.1:/`
   
>> * reset 
        
* connect to wifi *ssid:GOODJOB passwd:12345678*
* in web browser go to *http://192.168.1.1*
* set ssid and password to destanation router. the adminpasswd is for query and admin. 
* `http://{deviceip}/?pin={pinnum}&adminpasswd={adminpasswd}` to query pin status 
* `http://{deviceip}/?pin={pinnum}&value=[0|1|toggle]&adminpasswd={adminpasswd}` to set pin value 
* if you have a ssd1306 display connected(pin5=scl,pin4=sda) , the device ip should be display.(not tested)
* pull down pin13 will reset to default.