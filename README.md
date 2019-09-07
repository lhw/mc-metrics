# mc-metrics
## Prometheus Exporter for Minecraft servers

This small script exports some minimal information from a Minecraft server with RCON enabled as Prometheus metrics.
Depending on if Forge is available on the server this can be useful for watching performance metrics. If Forge is not available
this Exporter can sadly only tell you some basic information on player counts.

| Name | Description | Default |
| -------- | -------- | -------- |
| MINECRAFT_EXPORTER_PORT     | Port the Prometheus Exporter binds to     | 8080     |
| MINECRAFT_EXPORTER_INTERVAL | Interval in which to pull information from the minecraft RCON (in seconds) | 60 |
| MINECRAFT_RCON_HOST | Minecraft Server RCON IP | 127.0.0.1 |
| MINECRAFT_RCON_PORT | Minecraft Server RCON Port | 27015 |
| MINECRAFT_RCON_PASSWORD | Minecraft Server RCON Password | minecraft |
| MINECRAFT_RCON_TIMEOUT | Minecraft Server RCON Timeout (in seconds) | 5 |
| MINECRAFT_FORGE | Wether the Minecraft Server has Forge installed (true-ish value) | False |
