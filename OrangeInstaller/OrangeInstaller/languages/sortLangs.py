# sort langs files
import os

for file in os.listdir("."):
    if not "lang" in file or file.split(".")[-1] <> "py": continue
    f = open(file, "r")
    lines, part1, part2, part3 = [], [], [], []

    if not len(f.readlines()) > 1:
        for line in f.readlines():
            for line in line.split("\r"):
                lines.append(line)
        f = open(file, "w")
        f.write("".join(lines))
        f.close()

    for line in f.readlines():
        line = line.replace("\r","")
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
