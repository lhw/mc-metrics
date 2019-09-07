import asyncio

# So much noise, so much pollution
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR
[REGISTRY.unregister(c) for c in [PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR]]
from prometheus_client import Gauge
from prometheus_async.aio.web import start_http_server

from rcon import Connector

class Exporter:
    def __init__(self, interval=60, forge=True):
        self.interval = interval
        self.forge = forge
        self.cancelled = False
        self.online = Gauge('minecraft_online_players', 'Online Players')
        self.whitelist = Gauge('minecraft_whitelist_players', 'Whitelisted Players')
        self.banlist = Gauge('minecraft_banlist_players', 'Blacklisted Players')
        if forge:
            self.mean = Gauge('minecraft_mean_tick_time', 'Mean Tick Time', ['dim', 'sdim'])
            self.tps = Gauge('minecraft_mean_tps', 'Mean Ticks Per Second', ['dim', 'sdim'])

    async def start_web(self, port):
        print("Starting Prometheus Exporter on Port {}".format(port))
        await start_http_server(port=port)

    async def run(self, host, port, password, timeout):
        con = Connector()
        print("Connecting to {}:{}".format(host, port))
        await con.connect(host, port, password, timeout, self.forge)
        print("Starting exporter routine")
        while True:
            print("Updating data")
            self.online.set(await con.get_list())
            self.whitelist.set(await con.get_whitelist())
            self.banlist.set(await con.get_banlist())
            if self.forge:
                tps = await con.get_tps()
                for k, v in tps.items():
                    self.mean.labels(k[0], k[1]).set(v["mean"])
                    self.tps.labels(k[0], k[1]).set(v["tick"])
            print("Data update finished")
            if self.cancelled:
                break
            else:
                await asyncio.sleep(self.interval)

    def cancel(self):
        self.cancelled = True
