import asyncio
import re

from aiorcon.rcon import RCON

RE_TPS = re.compile(r'(?:Dim\s*(?P<dim>[-\d]+) \((?P<sdim>[^)]+).*?|Overall.*?)time: (?P<mean>[\d\.]+).*?TPS: (?P<tick>[\d\.]+)')
RE_LIST = re.compile(r'There are (?P<count>\d+)')


class Connector:
    async def connect(self, host, port, password, timeout=5, forge=True):
        self.rcon = await RCON.create(
            host, port, password,
            loop=asyncio.get_event_loop(),
            timeout=timeout,
            auto_reconnect_attempts=3,
            auto_reconnect_delay=5,
            auto_reconnect_cb=self.reconnect_cb,
            multiple_packet=False)
        self.forge = forge
        print("Initialized RCON connection")

    def reconnect_cb(*args):
        print("Lost RCON connection. Reconnecting")

    async def get_whitelist(self):
        return await self.get_list("whitelist ")

    async def get_banlist(self):
        return await self.get_list("banlist ")

    async def get_list(self, type="")
        resp = await self.rcon(f"{type}list")
        try:
            return int(RE_LIST.search(resp).group('count'))
        except:
            return 0

    async def get_tps(self):
        if not self.forge:
            return
        resp = await self.rcon('forge tps')
        stats = {}
        try:
            for m in RE_TPS.finditer(resp):
                if m.group('dim') is not None:
                    stats[(m.group('dim'), m.group('sdim'))] = {'mean': m.group('mean'), 'tick': m.group('tick')}
                else:
                    stats[(None, None)] = {'mean': m.group('mean'), 'tick': m.group('tick')}
        except Exception as e:
            print(e)
        return stats

