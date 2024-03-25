from cx_Freeze import setup, Executable

setup(
    name = "password_manager",
    version = "1.0",
    description = "инструмент работы с вашими паролями",
    executables = [Executable("Untitled-1.py")]
)