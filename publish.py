#!/usr/bin/env python3

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

    depth = str(os.path.relpath(root, docroot)).count('/')
    dir_title = str(os.path.relpath(root, docroot).split('/')[-1].replace('_', ' '))
    dir_path = None

    if(os.path.exists(Path(root, 'index.md'))):
        print('index found')
        dir_path = Path(root, 'index.md')
        dir_path = str(Path(os.path.relpath(root, docroot), 'index.md')).replace('/', '-').rsplit('.', 1)[0]

    if dir_title != '.':
        toc.append({'depth': depth, 'title': dir_title, 'path': dir_path, 'is_dir': True})

    for f in files:
        depth = str(Path(os.path.relpath(root, docroot), f)).count('/')

        src = Path(root, f)




        print("src: " + str(src))

        #print(f"Depth: {depth}")
        dst_filename = str(Path(os.path.relpath(root, docroot), f)).replace('/', '-')
        dst = Path(wikiroot, dst_filename)
        print("dst: " + str(dst))
        shutil.copy(src, dst)

        if str(f) == 'Home.md':
            continue

        if str(f) == '_Footer.md':
            continue

        if str(f) == '_Sidebar.md':
            continue

        if str(f) == 'index.md':
            continue


        title = str(f)
        path = dst_filename.rsplit('.', 1)[0]

        with open(src) as infile:
            firstline = infile.readline()
            if len(firstline) > 0:
                if firstline[0] == '#':
                    title = firstline[1:].strip()
                    print(title)



        toc.append({'depth': depth, 'title': title, 'path': path, 'is_dir': False})

print(toc)

with open(Path(wikiroot, '_Sidebar.md'), 'w') as outfile:
    for item in toc:
        if item['is_dir']:
            for _ in range(item['depth']):
                outfile.write('  ')
            if item['path'] != None:
                outfile.write(f'* [{ item["title"] }]({item["path"]})')
            else:
                outfile.write(f'* **{item["title"]}**')
        else:
            for _ in range(item['depth']):
                outfile.write('  ')
            outfile.write(f'* [{ item["title"] }]({item["path"]})')
        outfile.write('\n')

with open(Path(wikiroot, '_Footer.md'), 'w') as outfile:
    pass

with open(Path(wikiroot, 'Home.md'), 'w') as outfile:
    pass

