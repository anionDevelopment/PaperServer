import hashlib
import os
from pathlib import Path
import requests
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.TFCPS.Docker.TFCPS_CodeUnitSpecific_Docker import TFCPS_CodeUnitSpecific_Docker_Functions,TFCPS_CodeUnitSpecific_Docker_CLI

# See the comment in UpdateDependencies.py: the v2-api is sunset, so the v3-api is used.
_APIAddressOfPaper: str = "https://fill.papermc.io/v3/projects/paper"

# The name under which a build provides the server itself. A build also provides other artifacts (for example the
# mojang-mappings), which are not needed here.
_NameOfTheServerDownload: str = "server:default"

_TimeoutInSeconds: int = 30


def download_paperserver():
    script_file = str(Path(__file__).absolute())
    paper_version_file = GeneralUtilities.resolve_relative_path("../Resources/Dependencies/Paper/Version.txt", script_file)
    paper_version_file_content = GeneralUtilities.read_text_from_file(paper_version_file)
    paper_version = paper_version_file_content.split(";")[0]
    paper_version_build = paper_version_file_content.split(";")[1]
    GeneralUtilities.write_message_to_stdout(f"Download paper-server v{paper_version} (build {paper_version_build})...")
    folder_of_this_file = os.path.dirname(os.path.realpath(__file__))
    resource_folder = GeneralUtilities.resolve_relative_path("./Resources/PaperServer", folder_of_this_file)
    GeneralUtilities.ensure_directory_does_not_exist(resource_folder)
    GeneralUtilities.ensure_directory_exists(resource_folder)
    target_file = os.path.join(resource_folder, "PaperServer.jar")
    # The address of the file is asked for instead of being assembled, because the v3-api delivers the files from
    # another host than the api itself and the name of a file is not derivable from the version anymore.
    url = f"{_APIAddressOfPaper}/versions/{paper_version}/builds/{paper_version_build}"
    response = requests.get(url=url, timeout=_TimeoutInSeconds)
    response.raise_for_status()
    download = response.json()["downloads"][_NameOfTheServerDownload]
    # The file is downloaded with the same client as the api-request and not with urllib, because the host which
    # delivers the files answers the default user-agent of urllib with "403 Forbidden".
    with requests.get(download["url"], stream=True, timeout=_TimeoutInSeconds) as download_response:
        download_response.raise_for_status()
        with open(target_file, "wb") as target:
            for chunk in download_response.iter_content(chunk_size=1024*1024):
                target.write(chunk)
    verify_checksum(target_file, download["checksums"]["sha256"])


def verify_checksum(file: str, expected_sha256: str) -> None:
    """Ensures that the downloaded file is the one the api describes. Without this check a truncated or an exchanged
    download would end up in the image and would only be noticed when the server does not start."""
    actual_sha256 = hashlib.sha256(Path(file).read_bytes()).hexdigest()
    GeneralUtilities.assert_condition(actual_sha256 == expected_sha256, f"The checksum of \"{file}\" is \"{actual_sha256}\" but \"{expected_sha256}\" was expected.")


def common_tasks():
    tf:TFCPS_CodeUnitSpecific_Docker_Functions=TFCPS_CodeUnitSpecific_Docker_CLI.parse(__file__)
    download_paperserver()
    tf.do_common_tasks(tf.get_version_of_project())#codeunit-version should alsways be the same as project-version


if __name__ == "__main__":
    common_tasks()
