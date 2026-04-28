import sys
from entities.doctor import *

if len(sys.argv) > 1:
    message = sys.argv[1]
else:
    message = input("Enter message: ")

print("Message received from web:", message)