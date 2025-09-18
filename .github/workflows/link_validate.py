import os
import regex
from urllib.parse import quote as url

DIR = r'docs' 
PATTERN = r'(\[([^\]]+)\]\(([^)]+(.md)(#?[^\)]+)?)\))'#Capture group 1 is full link, CG 2 is display,  CG 3 is path, CG4 is heading

class File():
    '''Path/name storage.'''
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
    if file.name == 'index.md': # GH syntax not in PATTERN. This link we do not target.
        return
    with open(file.path,'r',encoding='utf-8') as f:
        data = f.read()
    links = regex.findall(pattern=PATTERN,string=data,flags=regex.UNICODE)
    if len(links) == 0:
        return
    else:
        compare_to = list(map(lambda x: url(x.name),files))
        for item in links:
            compare = regex.sub(pattern=r"^.*/",string=item[2],repl='',count=0,flags=regex.UNICODE)
            if compare in compare_to:
                continue
            else:
                data = data.replace(item[0],item[1])
            with open(file.path,'w',encoding='utf-8') as f:
                f.write(data)
    
files = File.index_markdown_files()

for item in files:
    try:
        check_markdown_links(item)
    except:
        print(f"Error with {item}")

