import os
import asyncio

from prom import Exporter

# Configuration parameters
EXPORTER_PORT = os.getenv("PROMETHEUS_EXPORTER_PORT", 8080)
EXPORTER_INTERVAL = os.getenv("PROMETHEUS_EXPORTER_INTERVAL", 60)

RCON_HOST = os.getenv("MINECRAFT_RCON_HOST", "127.0.0.1")
RCON_PORT = os.getenv("MINECRAFT_RCON_PORT", 27015)
RCON_PASSWORD = os.getenv("MINECRAFT_RCON_PASSWORD", "minecraft")
RCON_TIMEOUT = os.getenv("MINECRAFT_RCON_TIMEOUT", 5)

IS_FORGE = os.getenv("MINECRAFT_FORGE", False)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    #try:
    exp = Exporter(EXPORTER_PORT, EXPORTER_INTERVAL, IS_FORGE)
    loop.run_until_complete(exp.run(RCON_HOST, RCON_PORT, RCON_PASSWORD, RCON_TIMEOUT))
    #except Exception as e:
    #    print(e)
    #finally:
    #    loop.close()
