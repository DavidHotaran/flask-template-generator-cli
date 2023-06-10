import argparse
import os
from pathlib import Path
from colorama import Fore, Style, init
import subprocess
from subprocess import CalledProcessError
import sys

def main() -> None:
    '''Get the arguments from the cli. If the user wants to scaffold a new project,
    create the directory and clone down the sample project. If the user wants to create
    a route, model, schema, or all of the above, attemp to create file, ensuring we are in
    the correct directory.
    '''
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(title='scaffold commands')

    # create a project template; requires name of project from CLI
    scaffold = subparser.add_parser('scaffold', help='create a project template')
    scaffold.add_argument('project')

    # create route, model, schema, all
    create = subparser.add_parser('create', help='create a route, model, schema or all of the above files')
    create.add_argument('type', choices=['route', 'model', 'schema', 'all'])
    create.add_argument('-n', '--name', required=True)

    args = vars(parser.parse_args())

    if not args:
        parser.print_help()
        parser.exit()

    if args.get('project'):
        scaffold_project(args.get('project'))
    if args.get('type'):
        scaffold_type(args.get('type'), args.get('name'))

def scaffold_project(name: str):
    '''Create a directory from name given by user, and attempt to clone the example project.
    Steps:
    1. see if project name already exists, 
        1. if yes: exit
        2. if no: create project dir
    2. attempt to clone down project
        1. if successful: print success
        2. if no: print error and exit
    '''
    if os.path.exists(os.path.join(os.getcwd(), name)):
        print(Fore.RED + f"Error: project {name} already exists" + Style.RESET_ALL)
        sys.exit(1)
    else:
        os.mkdir(name)

    try:
        subprocess.run(['git', 'clone', 'https://github.com/DavidHotaran/flask-template.git', name], shell=True, check=True)
    except CalledProcessError:
        print(Fore.RED + "Error trying to clone down starter project, make sure you have git installed" + Style.RESET_ALL)
        sys.exit(1)

def scaffold_type(type: str, name: str) -> None:
    '''Depending on the type of file user wants to create, call `create_file`
    with the type and name.

    param: type:str = type of file to create (route, model, schema).
    param: name:str = the name of the file.
    '''
    if type == 'route':
        create_file(type, name)
    if type == 'model':
        create_file(type, name)
    if type == 'schema':
        create_file(type, name)
    if type == 'all':
        create_file('route', name)
        create_file('model', name)
        create_file('schema', name)

def create_file(type: str, name: str) -> None:
    '''Attempt to create the specified file. If the file name already exists,
    skip and let the user know.

    param: type:str = type of file to create (route, model, schema).
    param: name:str = the name of the file.
    '''
    dir = find_dir()
    path = os.path.join(dir, 'src', 'api', f'{type}s', f'{name}.py')
    file_name = Path(path)

    if file_name.exists():
        print(Fore.RED + f"File [{name}] already exists in [{type}]...skipping" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"Creating {type}: {path}" + Style.RESET_ALL)
        with open(path, 'w+') as file:
            file.close()

def find_dir() -> str:
    '''Find out if we are in a correct project to run the cli. We look
    to see if 'src' is in the path, or if we are at the top most level of the directory,
    if so we can create the file with everything
    before that.

    Returns the path to the files we need to "open" to create, or exits the program if
    we are not in the correct project directory.
    
    >>> '~/Documents/VS_CODE/hotaran-recipes-vite/hotaran-recipes/src/something/something'.split('src/')
    >>> ['~/Documents/VS_CODE/hotaran-recipes-vite/hotaran-recipes/', 'src/something/something.split']
    '''
    path = os.getcwd()
    dir = os.listdir()
    if 'src' in path:
        return path.split("src/")
    elif 'src' in dir:
        return ""
    else:
        print(Fore.RED + "Cannot scaffold, you are not in the project directory." + Style.RESET_ALL)
        exit(1)

if __name__ == '__main__':
    init()
    main()