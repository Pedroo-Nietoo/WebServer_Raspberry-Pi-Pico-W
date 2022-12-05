import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

ssid = 'Nicolly_NeoRede2.4'
password = '32474573'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Aguardando conexão...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Conectado em: {ip}')
    return ip

def open_socket(ip):
    #Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(): #-------------------- REVER DAQUI
    #Template html
    html = f"""
            <!DOCTYPE html>
             <html>
             <form action="./lighton">
             <input type="submit" value="Light on" />
             </form>
             <form action="./lightoff">
             <input type="submit" value="Light off" />
             </form>
             <p>LED está {state}</p>
             <p>Temperature é {temperature}</p>
             </body>
             </html>
             """
    return str(html)

def serve(connection):
    #Start a web page
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        client.close()
        
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
