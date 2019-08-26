import asyncio
import re

from aiorcon.rcon import RCON

RE_TPS = re.compile(r'(?:Dim\s*(?P<dim>[-\d]+) \((?P<sdim>[^)]+).*?|Overall.*?)time: (?P<mean>[\d\.]+).*?TPS: (?P<tick>[\d\.]+)')
RE_ONLINE = re.compile(r'There are (?P<online>\d)')

class Connector:
    async def connect(self, host, port, password, timeout=5, forge=True):
        self.rcon = await RCON.create(
            host, port, password,
            loop=asyncio.get_event_loop(),
            timeout=timeout,
            multiple_packet=False)
        self.forge = forge
        print("Initialized RCON connection")

    async def get_online(self):
        resp = await self.rcon('list')
        try:
            return int(RE_ONLINE.search(resp).group('online'))
        except:
            return 0

    async def get_tps(self):
        if not self.forge:
            return
        resp = await self.rcon('forge tps')
        stats = {}
        try:
            for match in RE_TPS.finditer(resp):
                if m.group('dim') is not None:
                    stats[(m.group('dim'), m.group('sdim'))] = {'mean': m.group('mean'), 'tick': m.group('tick')}
                else:
                    stats[(None, None)] = {'mean': m.group('mean'), 'tick': m.group('tick')}
        except:
            pass
        return stats

