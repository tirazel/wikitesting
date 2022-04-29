
import os

docroot = 'docs'

os.walk(docroot)

for root, dirs, files in os.walk(docroot):
  print(root)
  print(dirs)
  print(files)
