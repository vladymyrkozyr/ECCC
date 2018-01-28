import sys
import glob
import errno
import json


path = 'processed data/canenvironment/posts/*.json'   
files = glob.glob(path)  
big_json=[]
for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
    with open(name) as f: # No need to specify 'r': this is the default.
        post_info = json.load(f)
        post_info['id']=name[36:-5]
        print post_info
        big_json.append(post_info)
        #print f.read()
with open("posts.json", "w") as posts_file:
    json.dump(big_json, posts_file)
        






