# in cmd, run: py build.py build

import cx_Freeze

executables = [cx_Freeze.Executable("worldle-forever.pyw", icon="icon.ico", base=None, target_name='worldle-forever.exe')]

cx_Freeze.setup(
    name="Worldle Forever",
    options={"build_exe": {"packages":["pygame","os", "csv", "random", "unidecode"],
                           "include_files":["assets/"], "excludes":["numpy", "pip", "cx_Freeze"]}},
    executables = executables)