import asyncio

# So much noise, so much pollution
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR
[REGISTRY.unregister(c) for c in [PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR]]
from prometheus_client import start_http_server, Gauge

from rcon import Connector

class Exporter:
    def __init__(self, port, interval=60, forge=True):
        self.port = port
        self.interval = interval
        self.forge = forge
        self.online = Gauge('minecraft_online_players', 'Online Players')
        if forge:
            self.mean = Gauge('minecraft_mean_tick_time', 'Mean Tick Time', ['sdim', 'dim'])
            self.tps = Gauge('minecraft_mean_tps', 'Mean Ticks Per Second', ['sdim', 'dim'])

    async def run(self, host, port, password, timeout):
        print("Starting Prometheus Exporter on Port {}".format(self.port))
        start_http_server(self.port)
        con = Connector()
        print("Connecting to {}:{}".format(host, port))
        await con.connect(host, port, password, timeout, self.forge)
        print("Starting exporter routine")
        while True:
            print("Updating data")
            self.online.set(await con.get_online())
            if self.forge:
                tps = await con.get_tps()
                for k, v in tps.items():
                    self.mean.labels(k[0], k[1]).set(v["mean"])
                    self.tps.labels(k[0], k[1]).set(v["tick"])
            await asyncio.sleep(self.interval)

    def close(self):
        self.con.close()
