# sort langs files
import os

for file in os.listdir("."):
    if not "file" in file or file.split(".")[-1] <> "py": continue
    f = open(file, "rb")
    part1, part2, part3 = [], [], []

    for line in f.readlines():
        if line[0] == "#" or line.replace("\n", "")[-1] == "{":
            part1.append(line)
        elif line[-1] == "}":
            part3.append(line)
        else:
            part2.append(line)

    f = open(file, "w")
    f.write("".join(part1))
    f.write("".join(sorted(part2)))
    f.write("".join(part3))
