from bluepy import btle
import time

mac_address = "DC:54:75:D1:56:D1"
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

def byte_array_to_int(value):
	value = bytearray(value)
	value = int.from_bytes(value, byteorder="little", signed=True)
	return value
	
def read_button_var(service):
	button_char = service.getCharacteristics(CHARACTERISTIC_UUID)[0]
	button = button_char.read()
	button = byte_array_to_int(button)
	print(f"Button: {button}")
	
print("Connecting...")
nano_sense = btle.Peripheral(mac_address)

print("Discovering services...")
_ = nano_sen	se.services
bleService = nano_sense.getServiceByUUID(SERVICE_UUID)

print("Discovering characteristics...")
_ = bleService.getCharacteristics()

while True:
	print("\n")
	read_button_var(bleService)
	time.sleep(5)
