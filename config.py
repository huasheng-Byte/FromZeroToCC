from pathlib import Path

p = Path("./myfloder/myfile.txt")
abs_p = p.resolve()
print(abs_p)
print(type(abs_p))
