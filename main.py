import os
import asyncio

from prom import Exporter

# Configuration parameters
EXPORTER_PORT = int(os.getenv("MINECRAFT_EXPORTER_PORT", 8080))
EXPORTER_INTERVAL = int(os.getenv("MINECRAFT_EXPORTER_INTERVAL", 60))

RCON_HOST = os.getenv("MINECRAFT_RCON_HOST", "127.0.0.1")
RCON_PORT = int(os.getenv("MINECRAFT_RCON_PORT", 27015))
RCON_PASSWORD = os.getenv("MINECRAFT_RCON_PASSWORD", "minecraft")
RCON_TIMEOUT = int(os.getenv("MINECRAFT_RCON_TIMEOUT", 5))

IS_FORGE = bool(os.getenv("MINECRAFT_FORGE", False))


async def main():
    exp = Exporter(EXPORTER_INTERVAL, IS_FORGE)
    await exp.start_web(EXPORTER_PORT)
    await exp.run(RCON_HOST, RCON_PORT, RCON_PASSWORD, RCON_TIMEOUT)

if __name__ == '__main__':
    asyncio.run(main())
