import serial

import packet_encode as pe
import packet_decode as pd

# UART and XBee Configuration
# Arguments:
#   device - (string) serial device (e.g. /dev/ttyUSB0)
#   power - (int) XBee transmit power (0 to 4)
#   channel - (int) XBee channel (11 to 26) 
# Returns:
#   ser - (serial class) serial
def config(device,power,channel):
  ser = serial.Serial(port=device, timeout=5)

  # Set power
  if (power > 4) | (power < 0):
    print('Invalid power')
    return ser
  bytestr = pe.atcom_set('PL',(power).to_bytes(1,'big'))
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if success == 0:
      print('Error receiving response from AT set PL')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 

  print('Set power {}: success'.format(power))  

  # Set channel
  if (channel > 26) | (channel < 11):
    print('Invalid channel')
    return ser
  bytestr = pe.atcom_set('CH',(channel).to_bytes(1,'big'))
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if success == 0:
      print('Error receiving response from AT set CH')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 

  print('Set channel {}: success'.format(channel))

  # Write to NVM 
  bytestr = pe.atcom_query('WR')
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if success == 0:
      print('Error receiving response from AT query WR')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 

  print('Configuration saved to NVM')

  return ser
