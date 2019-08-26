# Fucking bullshit right here
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR
[REGISTRY.unregister(c) for c in [PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR]]
from prometheus_client import start_http_server, Gauge

from rcon import Connector

class Exporter:
    def __init__(self, port, interval=60, forge=True):
        self.online = Gauge('minecraft_online_players', 'Online Players')
        if forge:
            self.mean = Gauge('minecraft_mean_tick_time', 'Mean Tick Time', ['sdim', 'dim'])
            self.tps = Gauge('minecraft_mean_tps', 'Mean Ticks Per Second', ['sdim', 'dim'])
        self.forge = forge
        self.interval = interval

    async def run(self, host, port, password, timeout):
        start_http_server(port)
        con = Connector()
        await con.connect(host, port, password, timeout, self.forge)
        while True:
            self.online.set(await con.get_online())
            for k, v in await con.get_tps():
                mean.labels(k[0], k[1]).set(v["mean"])
                tps.labels(k[0], k[1]).set(v["tick"])
            asyncio.sleep(self.interval)
