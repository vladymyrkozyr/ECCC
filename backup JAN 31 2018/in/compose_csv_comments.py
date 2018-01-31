import sys
import glob
import errno
import json

rootPath='processed data/ressourcesnaturellescanada/'
path = rootPath+'comments/*.json'   
files = glob.glob(path)  
big_json=[]
for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
    with open(name) as f: # No need to specify 'r': this is the default.
        post_info = json.load(f)
        for c in post_info:
            c['post_id']=name[51:-14]
            big_json.append(c)
        #print f.read()
with open(rootPath+"comments.json", "w") as posts_file:
    json.dump(big_json, posts_file)
        






