import os
import sys
import json
import shutil
import colors


def make_and_move_to_dir(origin, new_dir):
    """
    Make a new folder when needed and moves files and folders to specified path
    """
    if not os.path.exists(new_dir):
        print colors.blue("[NOTICE]") + \
            " creating new folder for: %s" % os.path.basename(new_dir)

        os.mkdir(new_dir)

    print colors.blue("[NOTICE]") + \
        " moving %s to %s" % (os.path.basename(origin), new_dir)

    try:
        shutil.move(origin, new_dir)
    except IOError:
        sys.exit(colors.yellow("[ERROR]") + " not able to find file")
    except shutil.Error:
        sys.exit(colors.yellow("[ERROR]") + " %s already present in %s. "
                 "Please remove the file." % (origin, new_dir))


def create_symlink(origin, new_dir):
    """
    Creates symlink for a file or directory to the specified path
    src: where is the file/folder located
    dst: where should the symlink be (also known as the origin)
    """
    try:
        src = os.path.abspath(new_dir) + "/" + os.path.basename(origin)
        dst = origin

        print colors.blue("[NOTICE]") + \
            " creating symlink for: %s to %s" % (os.path.basename(origin), src)

        os.symlink(src, dst)
    except OSError:
        sys.exit(colors.yellow("[ERROR]") + " symlinking failed, file exists")


def check_args(args, expected):
    """
    Check if the list of the arguments is of the correct length
    """
    arg_length = len(args)
    if arg_length != expected:
        sys.exit(
            colors.red("[ERROR]") + " incorrect number of arguments, "
            "expected %r, given %r" % (expected, arg_length))
    else:
        return True


def create_config_file():
    """
    Creates the config file in the home folder
    """

    config_location = os.path.expanduser("~") + "/.dotconfig"

    if not os.path.exists(config_location):
        data = """
        {
            "files" : {},
            "dot_path" : ""
        }
        """

        try:
            dotconfig = open(config_location, 'w')
            dotconfig.write(data)
            dotconfig.close()
            return True
        except IOError:
            sys.exit(colors.yellow("[ERROR]") + " not able to write to data file")
    else:
        return True


def get_dotconfig(path=None):
    """
    Get the data from the .dotconfig file
    """
    if not path:
        path = os.path.expanduser("~") + "/.dotconfig"

    try:
        data_file = open(path)
        data = json.load(data_file)
        data_file.close()
    except IOError:
        sys.exit(colors.yellow("[ERROR]") + " not able to find data file")
    except ValueError:
        sys.exit(colors.yellow("[ERROR]") + " not able to parse data file")

    return data


def set_dotconfig(data, path=None):
    """
    Set the data for the .dotconfig file
    """
    if not path:
        path = os.path.expanduser("~") + "/.dotconfig"

    try:
        write_data = json.dumps(data, sort_keys=True, indent=4)
        data_file = open(path, 'w')
        data_file.write(write_data)
        data_file.close()
    except IOError:
        sys.exit(colors.yellow("[ERROR]") + " not able to write to data file")


def get_dot_path():
    """
    Get the path of where the dotfiles are located. This is the location of the
    files and backup folders.
    """
    data = get_dotconfig()

    if not data['dot_path']:
        sys.exit(colors.yellow("[ERROR]") + " path not found in config file")

    return (os.path.expanduser("~") + data['dot_path'])


def set_dot_path(path):
    """
    Set the path of where the dotfiles are located. This will be the location
    of the files and backup folders.
    """
    data = get_dotconfig()

    try:
        data.update({'dot_path': path})
    except AttributeError:
        sys.exit(colors.yellow("[ERROR]") + " not able to update .dotconfig"
                               "file. Check if the integrity of the file.")

    set_dotconfig(data)

    print colors.blue("[NOTICE]") + " set %s as path in .dotconfig" % path
