---
name: product-knowledge
description: What PaperServer is, how this repository is structured and which mechanisms exist for building it. Use this before fixing a defect or developing a feature in this repository, to know where things belong and how to verify a change.
---

# PaperServer

PaperServer is a docker-image which runs a [Paper](https://papermc.io)-server (a minecraft-server) in a
container. The repository contains no application-sourcecode of its own: what it maintains is the image and the
question which version of Paper the image contains.

## Structure of the repository

The repository follows the "common project structure". Use the `work-with-common-project-structure`-skill when
you need the details of that structure.

There is one code-unit, `PaperServer`, which is the image-definition.

## The version of Paper

Two scripts belong together here:

- `PaperServer/Other/UpdateDependencies.py` asks the api of papermc for the newest version and writes it into
  `PaperServer/Other/Resources/Dependencies/Paper/Version.txt` in the form `<version>;<build>`.
- `PaperServer/Other/CommonTasks.py` downloads exactly that version while building the image.

Both use the **v3-api** under `https://fill.papermc.io/v3`. The v2-api is sunset and answers every request with
an error. Three things are structured differently there than in the v2-api, and each of them silently produces
a wrong result when it is overlooked:

- The versions are **grouped by their version-family**, and both the families and the versions inside a family
  are ordered with the **newest first** (the v2-api returned one flat list with the newest at the end).
- A build is identified by `id`, not by `build`.
- The jar-file is delivered from another host and its name is not derivable from the version, so the address
  has to be taken from the answer of the api instead of being assembled.

Only released versions (no `-rc`, no `-pre`) and only builds in the channel `STABLE` are used. The download is
verified against the sha256-checksum which the api states, so a truncated download does not end up in the image.

## Building

`scbuildcodeunits` builds everything. The task `task bb` (`BaseBuildAllCodeunits`) does the same.

For the single code-unit, run the scripts in `PaperServer/Other/Build` and `PaperServer/Other/QualityCheck`, and
run them from the folder they are located in.
