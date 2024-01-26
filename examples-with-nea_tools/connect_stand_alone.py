"""
Connects and disconnects to/from neaSNOM as stand-alone script.
To control neaSNOM from console, remove `nea_tools.disconnect()`
and run in prompt: 
`python -i stand_alone.py`
Requires full SDK to be enabled
"""

import asyncio
import nea_tools

# get dll files from server location /usr/share/neaspec/windows/Application Files/
# or with explorer of client: "\\nea-server\updates\Application Files\"
path_to_dll = ""
fingerprint = None
host = 'nea-server'

# nea_tools.set_output(None) # turn off logging

# connecting and creating module neaspec on success
asyncio.run(nea_tools.connect(host, fingerprint, path_to_dll))
from neaspec import context

print("M1A =", context.Microscope.Py.MechanicalAmplitude)

# Don't forget to disconnect
print('\nDisconnecting')
nea_tools.disconnect()
