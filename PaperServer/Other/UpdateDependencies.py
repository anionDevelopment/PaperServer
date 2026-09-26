from pathlib import Path
import requests
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore
from ScriptCollection.TFCPS.TFCPS_Tools_General import TFCPS_Tools_General

# The v2-api of papermc is sunset ("This API version has been sunset and is no longer available"), so the v3-api is
# used. Its answers are structured differently: the versions are grouped by their version-family and both the
# families and the versions inside a family are ordered with the newest first (the v2-api returned one flat list
# with the newest at the end), and a build is identified by "id" instead of by "build".
_APIAddressOfPaper: str = "https://fill.papermc.io/v3/projects/paper"

# Builds which are not in this channel are not finished releases and must not be delivered.
_StableChannel: str = "STABLE"

_TimeoutInSeconds: int = 30


def get_released_version_numbers(timeout_in_seconds: int) -> list[str]:
    response = requests.get(url=_APIAddressOfPaper, timeout=timeout_in_seconds)
    response.raise_for_status()
    versions_by_family = response.json()["versions"]
    return [version for versions_of_family in versions_by_family.values() for version in versions_of_family if is_released_version(version)]


def is_released_version(version: str) -> bool:
    lowered_version = version.lower()
    return not ("-rc" in lowered_version or "-pre" in lowered_version or "-snapshot" in lowered_version)


def get_latest_stable_build_number(version_number: str, timeout_in_seconds: int) -> str | None:
    url = f"{_APIAddressOfPaper}/versions/{version_number}/builds"
    response = requests.get(url=url, timeout=timeout_in_seconds)
    response.raise_for_status()
    builds = response.json()
    for build in builds:
        if build["channel"] == _StableChannel:
            return str(build["id"])
    return None


def get_latest_paper_version() -> str:
    # A new minecraft-version is usually listed before paper has a stable build for it (it has only builds in the
    # channels "ALPHA" or "BETA" at the beginning), so the newest version which already has a stable build is used.
    for version_number in get_released_version_numbers(_TimeoutInSeconds):
        build_number = get_latest_stable_build_number(version_number, _TimeoutInSeconds)
        if build_number is not None:
            return f"{version_number};{build_number}"
    raise ValueError(f"No released version with a build in the channel \"{_StableChannel}\" was found under \"{_APIAddressOfPaper}\".")


def update_dependencies():
    script_file = str(Path(__file__).absolute())
    sc = ScriptCollectionCore()
    TFCPS_Tools_General(sc).update_dependency_in_resources_folder(script_file, "Paper", get_latest_paper_version())


if __name__ == "__main__":
    update_dependencies()
