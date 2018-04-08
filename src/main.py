import logging, shutil, sys, os

'''
    Imports a python file from a string path
'''
def modular_import(s):
    # remove .py file extension if exists
    if s.endswith('.py'):
        s = s[:s.index('.py')]

    # append to path if not in current directory
    if '/' in s:
        sys.path.append(s[:s.rindex('/')])

    # import file
    __import__(s[s.rindex('/') + 1:] if '/' in s else s)

'''
    Finds a file or folder named the string
'''
def find_file(s, location, suffix = '.py'):
    files = list()
    for filename in os.listdir(location):
        if not os.path.isfile(location + '/' + filename):
            files.extend(find_file(s, location + '/' + filename))
        elif s in filename and filename.endswith(suffix):
            files.append(location + '/' + filename)
    return files

class commands:
    '''
        Displays a help menu
    '''
    def help(args, examples = True):
        if len(args) == 0:
            # if no arguments for --help are specified, go through each arg definition
            for definition in main.argument_definitions:
                commands.help([definition['name'][0]], examples = False)
        else:
            # for each argument in args, print the help menu
            for argument in args:
                definition = main.get_argument(argument.lstrip('-').lower())

                # if the argument definition exists
                if not definition is False:
                    # print out a preformatted help menu
                    print(('[-' + definition['name'][0] + '/--' + definition['name'][1] + ']').ljust(20) + definition['help'])

                    # if it should display examples, do it
                    if examples:
                        print('    Examples:')
                        for example in definition['examples']:
                            print('      ' + sys.argv[0] + ' <-' + definition['name'][0] + '/--' + definition['name'][1] + '> ' + example)
                        print()
                else:
                    logging.error('Error: That parameter does not exist.', end = True)
            pass

    '''
        Executes the script(s) provided in `args`
    '''
    def execute(args):
        if len(args) == 0:
            print(sys.argv[0] + ' ' + sys.argv[1] + ' [scripts]')
        base_directory = '../data/'

        # copy the temporary lib file over
        shutil.copyfile('./utils.py', base_directory + 'utils.py')

        for arg in args:
            files = find_file(arg, '../data')
            if len(files) is 0:
                logging.error('Warning: No scripts found for search term "' + arg + '"')
            else:
                # generate a list of single executable files
                history = {'files' : 0, 'folders' : 0}
                for filename in files:
                    if filename.endswith('.py'):
                        history['files'] += 1
                    else:
                        history['folders'] += 1

                # don't continue if there's more than one executable file
                if history['files'] > 1 or history['folders']:
                    logging.error('Warning: Search term "' + arg + '" is ambiguous')
                else:
                    for filename in files:
                        if filename.endswith('.py'):
                            try:
                                modular_import(filename)
                            except Exception as e:
                                logging.error('Warning: Execution of script ' + filename + ' failed at runtime\n    ' + str(e))

                        else:
                            for suffix in os.listdir(filename):
                                try:
                                    modular_import(filename + '/' + suffix)
                                except Exception as e:
                                    logging.error('Warning: Execution of script ' + (filename + '/' + suffix) + ' failed at runtime\n    ' + str(e))

        # remove the temp utils lib file
        os.remove(base_directory + 'utils.py')

    '''
        Lists all available scraping scripts
    '''
    def list(args, depth = None, recursive = True, path_prefix = '../data'):
        # if commands.list is being called from the argument processor
        if depth is None:
            # recursively list files in path_prefix
            print('[scripts]')
            commands.list([''], depth = 2)
        else:
            # get a list of files in the directory that is being listed
            filenames = os.listdir(path_prefix + args[0])

            # reverse it so the list is alphabetically sorted, starting with files
            filenames.reverse()

            # iterate filenames
            for filename in filenames:
                # if the current filename is not the current directory
                if not filename in ['.', '__pycache__']:
                    # if the current filename is a directory
                    if not os.path.isfile(path_prefix + '/' + args[0] + '/' + filename):
                        # print the filename, formatted as a directory
                        print(' ' * (depth - 2) + '|─[' + filename + ']')

                        # then list files in that directory
                        commands.list([args[0] + '/' + filename], depth = depth + 2, path_prefix = path_prefix)
                    else:
                        # print the filename if it ends with ".py", formatted as a file
                        if filename.endswith('.py'):
                            print(' ' * (depth - 2) + '| ' + filename[:filename.rindex('.')])

class main:
    default_argument = '--help'
    argument_definitions = [
        {
            'name' : ['h', 'help'],
            'help' : 'Displays this help menu',
            'examples' : [
                '',
                '[arguments]',
                'execute',
                'execute help'
            ],
            'call' : commands.help
        },
        {
            'name' : ['e', 'execute'],
            'help' : 'Executes scripts provided as parameters',
            'examples' : [
                '[scripts]',
                'google',
                'google duckduckgo'
            ],
            'call' : commands.execute
        },
        {
            'name' : ['l', 'list'],
            'help' : 'Lists all available scripts',
            'examples' : [
                ''
            ],
            'call' : commands.list
        }
    ]

    '''
        Returns an argument by name, or False
    '''
    def get_argument(arg):
        for definition in main.argument_definitions:
            for name in definition['name']:
                if name.lower() == arg:
                    # found a match
                    return definition

        return False

    '''
        Executes the handler of the given argument

        Returns a boolean, True or False (for found or not found)
    '''
    def execute(args, sysargs = True):
        # copy array so that the value does not alter
        args = args[:]

        # if the array is from sys.argv, remove the first (unneeded) element
        if sysargs:
            args.pop(0)

        # get the argument to execute
        arg = (args.pop(0) if len(args) is not 0 else main.default_argument).lstrip('-').lower()

        # search argument definitions (case insensitive) for the argument
        definition = main.get_argument(arg)

        # execute the handler if the argument exists
        if not definition is False:
            definition['call'](args)
            return True

        # otherwise, exit
        return False

if __name__ == "__main__":
    if not main.execute(sys.argv):
        logging.error('Error: Unknown argument. Try ' + sys.argv[0] + ' --help', end = True)
