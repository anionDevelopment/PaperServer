# PaperServer

## Development-state

![Development-state](https://img.shields.io/badge/development--state-maintenance%20updates%20only-green)

The underlying [Paper](https://papermc.io)-server will be developed actively.

## Purpose

[PaperServer](https://projects.aniondev.de/PublicProjects/Images/PaperServer) is a docker-image for simply running a [Paper](https://papermc.io)-server in a docker-container.

## Usage

### Volumes

There are 3 volumes-paths:

- `/Workspace/Shared/Configuration`
- `/Workspace/Shared/Data`
- `/Workspace/Shared/Logs`

### Environment-variables

The following environment-variables are available:

- `accept_minecraft_eula`
- `java_xms`
- `java_xmx`

`accept_minecraft_eula` must be set to `true`, otherwise the Paper-server refuses to start. Setting it to `true` means that you accept the [Minecraft-EULA](https://www.minecraft.net/eula). Technically this writes `eula=true` to `eula.txt` in the configuration-folder on every start of the container. `java_xms` and `java_xmx` are not required.

### Example

See the [minimal example `docker-compose.yml`](https://projects.aniondev.de/PublicProjects/Images/PaperServer/-/blob/main/PaperServer/Other/Examples/MinimalDockerComposeFile/docker-compose.yml) for an example how to use this image.
