import binascii
import os
random_id = os.urandom(4)

print type(random_id)
print binascii.hexlify(random_id)