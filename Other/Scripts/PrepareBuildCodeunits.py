import os
from ScriptCollection.TFCPS.TFCPS_Generic import TFCPS_Generic_Functions, TFCPS_Generic_CLI

def prepare_build_codeunits():
    t :TFCPS_Generic_Functions= TFCPS_Generic_CLI().parse(__file__)
    t.tfcps_Tools_General.generate_tasksfile_from_workspace_file(t.repository_folder)
    t.tfcps_Tools_General.generate_codeunits_overview_diagram(t.repository_folder)
    t.tfcps_Tools_General.generate_svg_files_from_plantuml_files_for_repository(t.repository_folder,t.use_cache())


if __name__ == "__main__":
    prepare_build_codeunits()
