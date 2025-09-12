import os
import regex
from urllib.parse import quote as url

DIR = r'docs'

class File():
    def __init__(self,path,name) -> None:
        self.path: str = path
        self.name: str = name

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name

    @staticmethod
    def index_markdown_files(dir = DIR) -> list:
        '''Indexes all markdown files based off an input directory.'''
        output = []
        for (dir_path, dir_names, file_names) in os.walk(DIR):
           for file in file_names:
               if file.endswith('.md'):
                   output.append(File(path=os.path.join(dir_path,file),name=file))
        return output

def check_markdown_links(file: File):
    '''Checks local markdown links. If inaccurate, removes them.'''
    with open(file.path,'r',encoding='utf-8') as f:
        data = f.read()
    links = regex.findall(pattern=r'\[([^\]]+)\]\(([^)]+(.md))\)',string=data)
    if len(links) == 0:
        return
    else:
        compare_to = list(map(lambda x: url(x.name),files))
        for item in links:
            compare = regex.sub(pattern=r"^.*/",string=url(item[1]),repl='',count=0,flags=regex.UNICODE)
            if compare not in compare_to:
                data = regex.sub(pattern=r'\[([^\]]+)\]\(([^)]+(.md))\)',string=data,repl=r'\1',count=0,flags=regex.UNICODE)
        with open(file.path,'w',encoding='utf-8') as f:
            f.write(data)
    
files = File.index_markdown_files()

for item in files:
    try:
        check_markdown_links(item)
    except:
        print(f"Error with {item}")

