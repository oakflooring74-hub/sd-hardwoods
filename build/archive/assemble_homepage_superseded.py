SCRATCH = r"C:\Users\oakfl\AppData\Local\Temp\claude\c--FLOORING-TEST-SITE\43117800-38d9-4403-8a3c-69454d90bbc0\scratchpad"
OUT = r"C:\FLOORING TEST SITE\index.new.html"

with open(SCRATCH + r"\new_head_fragment.html", encoding="utf-8") as f:
    head = f.read()
with open(SCRATCH + r"\body_skeleton.html", encoding="utf-8") as f:
    body = f.read()
with open(SCRATCH + r"\gallery_grid_fragment.html", encoding="utf-8") as f:
    gallery = f.read()

body = body.replace("__GALLERY_GRID__", gallery)

# add <base> for correct local preview of relative asset paths (image srcs, relative links)
head = head.replace(
    '<meta charset="utf-8">',
    '<meta charset="utf-8"><base href="https://www.sdhardwoods.com/">'
)

doc = "<!DOCTYPE html><html lang=\"en\">\n" + head + "\n" + body

with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)

print(f"Wrote {OUT}, {len(doc)} chars")
