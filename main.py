import os
import asyncio

from prom import Exporter

from prometheus_async.aio.web import start_http_server

# Configuration parameters
EXPORTER_PORT = int(os.getenv("MINECRAFT_EXPORTER_PORT", 8080))
EXPORTER_INTERVAL = int(os.getenv("MINECRAFT_EXPORTER_INTERVAL", 60))

RCON_HOST = os.getenv("MINECRAFT_RCON_HOST", "127.0.0.1")
RCON_PORT = int(os.getenv("MINECRAFT_RCON_PORT", 27015))
RCON_PASSWORD = os.getenv("MINECRAFT_RCON_PASSWORD", "minecraft")
RCON_TIMEOUT = int(os.getenv("MINECRAFT_RCON_TIMEOUT", 5))

IS_FORGE = bool(os.getenv("MINECRAFT_FORGE", False))

if __name__ == '__main__':
    print("Starting Prometheus Exporter on Port {}".format(EXPORTER_PORT))
    asyncio.ensure_future(start_http_server(port=EXPORTER_PORT))
    exp = Exporter(EXPORTER_INTERVAL, IS_FORGE)
    asyncio.run(exp.run(RCON_HOST, RCON_PORT, RCON_PASSWORD, RCON_TIMEOUT))
