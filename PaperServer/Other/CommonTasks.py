import os
import urllib
from pathlib import Path
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.TFCPS.Docker.TFCPS_CodeUnitSpecific_Docker import TFCPS_CodeUnitSpecific_Docker_Functions,TFCPS_CodeUnitSpecific_Docker_CLI



def download_paperserver():
    script_file = str(Path(__file__).absolute())
    paper_version_file = GeneralUtilities.resolve_relative_path(f"../Resources/Dependencies/Paper/Version.txt", script_file)
    paper_version_file_content = GeneralUtilities.read_text_from_file(paper_version_file)
    paper_version = paper_version_file_content.split(";")[0]
    paper_version_build = paper_version_file_content.split(";")[1]
    GeneralUtilities.write_message_to_stdout(f"Download paper-server v{paper_version} (build {paper_version_build})...")
    folder_of_this_file = os.path.dirname(os.path.realpath(__file__))
    resource_folder = GeneralUtilities.resolve_relative_path("./Resources/PaperServer", folder_of_this_file)
    GeneralUtilities.ensure_directory_does_not_exist(resource_folder)
    GeneralUtilities.ensure_directory_exists(resource_folder)
    target_file = os.path.join(resource_folder, "PaperServer.jar")
    urllib.request.urlretrieve("https://api.papermc.io/v2/projects/paper/versions" + f"/{paper_version}/builds/{paper_version_build}/downloads/paper-{paper_version}-{paper_version_build}.jar", target_file)


def common_tasks():
    tf:TFCPS_CodeUnitSpecific_Docker_Functions=TFCPS_CodeUnitSpecific_Docker_CLI.parse(__file__)
    download_paperserver()
    tf.do_common_tasks(tf.get_version_of_project())#codeunit-version should alsways be the same as project-version
    tf.take_readmefile_from_main_readmefile_of_repository(file)


if __name__ == "__main__":
    common_tasks()
