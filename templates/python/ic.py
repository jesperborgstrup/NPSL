{% set output_dest, package = "ic.py", "client" %}

from client import Client
from clientinterface import ClientInterface
c = Client(interface=ClientInterface())
c.connect()
