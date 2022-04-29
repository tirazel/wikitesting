
import os
import shutil
from pathlib import Path

docroot = 'docs'
wikiroot = 'wiki'

for filename in os.listdir(wikiroot):
    file_path = os.path.join(wikiroot, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


toc = []

for root, dirs, files in os.walk(docroot):
    #print(os.path.relpath(root, docroot))
    print(f'root: {root}')
    #print(dirs)

    for f in files:
        if str(f) == 'index.md':
            continue

        src = Path(root, f)
        #print("src: " + str(src))
        depth = str(Path(os.path.relpath(root, docroot), f)).count('/')
        #print(f"Depth: {depth}")
        dst_filename = str(Path(os.path.relpath(root, docroot), f)).replace('/', '-')
        dst = Path(wikiroot, dst_filename)
        #print("dst: " + str(dst))
        shutil.copy(src, dst)

        title = str(f)
        path = dst_filename

        with open(src) as infile:
            firstline = infile.readline()
            if len(firstline) > 0:
                if firstline[0] == '#':
                    title = firstline[1:].strip()
                    print(title)



        toc.append({'depth': depth, 'title': title, 'path': path})

print(toc)

with open(Path(wikiroot, '_Sidebar.md'), 'w') as outfile:
    for item in toc:
        for _ in range(item['depth']):
            outfile.write('  ')
        outfile.write(f'* [{ item["title"] }]({item["path"]})')
        outfile.write('\n')


