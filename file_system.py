def run_file_system():
    dictionary = {'root': {'bin': {}}}
    current_direct = 'root'
    direct_path = '/root/'

    def return_current():  # helper function
        return direct_path.split('/')[-2]

    def ls(dictionary, path):
        current = return_current()
        for key, value in dictionary.items():
            if value != 'file':
                if len(path) == 1 and current == path[0] and key == path[0]:
                    # if length of path is 1, the last
                    # element is the final element in path,
                    # and path element is key, then print values
                    for item in value.keys():
                        print(item)
                elif key == path[0]:
                    return ls(value, path[1:])

    def cd(dictionary, path_list1, path_list2, current, path, direct_path):
        for key, value in dictionary.items():
            if value != 'file':
                if len(path) == 1 and current == path[0]:
                    if path_list1[0] in value.keys():
                        if value[path_list1[0]] == 'file':
                            return None
                        else:
                            if len(path_list1) == 1:
                                current = path_list1[0]
                                path_list2 = '/'.join([i for i in path_list2 if i != ''])
                                direct_path += f'{path_list2}/'
                                return (current, direct_path)
                            else:
                                # this recursive call moves to desired location
                                return cd(value, path=path, path_list1=path_list1[1:], current=current,
                                          path_list2=path_list2, direct_path=direct_path)
                elif key == path[0]:
                    # this recursive call moves to current location
                    return cd(value, path_list1=path_list1, current=current, path=path[1:], path_list2=path_list2,
                              direct_path=direct_path)

    def cd_back(direct):
        if direct != ['', 'root', '']:
            current = direct[-2]#-2 because when split in call the string slash becomes '' in list
            direct = '/'.join(direct[:-2]) + '/'
            return current, direct
        else:
            current = 'root'
            direct = '/root/'
            return current, direct

    def cd_allback(direct=direct_path.split('/')):
        current = direct[1]#takes back to index 1, origional directory, index 0 is ''
        direct = f'/{direct[1]}/'
        return current, direct

    def mkdir(dictionary, path, command):
        current = return_current()
        if '/' in command:
            print('error')
            return
        for key, value in dictionary.items():
            if value != 'file':
                if len(path) == 1 and current == path[0] and key == path[0]:
                    if command in value.keys():
                        print('directory already exists')
                        return
                    value[command] = {}
                    return
                elif key == path[0]:
                    return mkdir(value, path[1:], command)#moves through the path list by increment of 1

    def touch(dictionary, path, command):
        current = return_current()
        for key, value in dictionary.items():
            if value != 'file':
                if len(path) == 1 and current == path[0] and key == path[0]:
                    value[command] = 'file'#set value as 'file' to represent a file
                    return
                elif key == path[0]:
                    return touch(value, path[1:], command)

    def rm(dictionary, path, command):
        current = return_current()
        for key, value in dictionary.items():
            if value != 'file':
                if len(path) == 1 and current == path[0] and key == path[0]:
                    if command not in value.keys():
                        print('file doesn\'t exist')
                        return
                    elif value[command] != 'file':#if the desired entry is a file, don't attempt to enter it
                        print('not a file')
                        return
                    else:
                        del value[command]
                        return
                elif key == path[0]:
                    return rm(value, path[1:], command)

    def locate(dictionary, path, search, condition=False, path_string=''):
        current = return_current()
        for key, value in dictionary.items():
            if value == 'file' and condition == True:
                if search in key:
                    print('/' + path_string + key)
            if len(path) == 1 and value != 'file':
                if path_string == '' and key == 'root':
                    path_string += ''
                else:
                    path_string += f'{key}/'
                locate(value, path, search, condition=True, path_string=path_string)#don't use return because want to iterate over all key value pairs
                path_string = '/'.join(path_string.split('/')[:-2]) + '/'
            elif key == path[0]:
                return locate(value, path[1:], search, condition, path_string='')

    def pwd():  # helper function
        print(direct_path[5:])#start from 5 to start from slash

    def return_input():  # helper function
        return input('[cmsc201 proj3]$ ')

    command = None
    while command != 'exit':
        command = return_input()
        if command == 'ls':
            print(f'Contents for {direct_path[5:]}')
            ls(dictionary, direct_path.split('/')[1:-1])#[1,-1] to remove the slashes that become '' in list
        elif command == 'cd /':
            current_direct, direct_path = cd_allback()
        elif command == 'cd ..':
            current_direct, direct_path = cd_back(direct_path.split('/'))
        elif command[:3] == 'cd ':
            if len(command.split(' ')) != 2:
                print('error')
            else:
                if cd(dictionary, path_list1=[i for i in command[3:].split('/') if i != ''],
                      path_list2=command[3:].split('/'), current=direct_path.split('/')[-2],
                      path=direct_path.split('/')[1:-1], direct_path=direct_path) == None:
                    print('no directory')
                else:
                    current_direct, direct_path = cd(dictionary,
                                                     path_list1=[i for i in command[3:].split('/') if i != ''],
                                                     path_list2=command[3:].split('/'),
                                                     current=direct_path.split('/')[-2],
                                                     path=direct_path.split('/')[1:-1], direct_path=direct_path)
        elif command[:6] == 'mkdir ':
            if len(command.split(' ')) != 2:
                print('error')
            else:
                mkdir(dictionary, direct_path.split('/')[1:-1], command[6:])
        elif command[:6] == 'touch ':
            if len(command.split(' ')) != 2:
                print('error')
            else:
                touch(dictionary, direct_path.split('/')[1:-1], command[6:])
        elif command[:3] == 'rm ':
            if len(command.split(' ')) != 2:
                print('error')
            else:
                rm(dictionary, direct_path.split('/')[1:-1], command[3:])
        elif command[:7] == 'locate ':
            if len(command.split(' ')) != 2:
                print('error')
            else:
                locate(dictionary, direct_path.split('/')[1:-1], command[7:])
        elif command == 'pwd':
            pwd()
        elif command == 'exit':
            print()
        else:
            print('error')


if __name__ == "__main__":
    run_file_system()
