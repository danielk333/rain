import pathlib

md_doc = """

# API

"""

path = pathlib.Path(".") / "src" / "rain"
output = pathlib.Path(".") / "docs" / "api.md"

for file in path.glob("*.py"):
    if file.stem.startswith("__"):
        continue
    md_doc += f"::: rain.{file.stem}\n\n"

with open(output, "w") as fh:
    fh.write(md_doc)