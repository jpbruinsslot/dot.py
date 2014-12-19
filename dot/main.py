import os
import sys
import shutil
import colors
import helpers


def run_command(cmd, args):
    if not cmd:
        run()

    elif cmd == "init":
        init()

    elif cmd == "add":
        add(args)

    elif cmd == "rm":
        remove(args)

    elif cmd == "list":
        show_list()

    else:
        sys.exit(colors.yellow("[ERROR]") + " command was not recognized")


def run():
    """
    Main function that will run the script
    """
    if not os.path.exists("backup"):
        sys.exit(colors.blue("[NOTICE]") +
                 " no backup folder found, please run the command 'dot init'")

    if not os.path.exists("files"):
        sys.exit(colors.blue("[NOTICE]") +
                 " no files folder found, please run the command 'dot init'")

    data = helpers.get_dotconfig()

    for key, value in data['files'].iteritems():

        print colors.red("***") + \
            colors.green(" Creating references for: %s " % key) + \
            colors.red("***")

        origin = os.path.expanduser(value)

        if not os.path.exists(origin):
            print colors.blue("[NOTICE]") + \
                " %s does not exist for %s" % (value, key)
            continue

        if os.path.islink(origin):
            print colors.blue("[NOTICE]") + \
                " symlink is already present for: %s" % key
            continue

        """
        When we are running this script on a machine, we want to make sure
        that files that are present in the files folder, but not yet symlinked
        on the machine, are moved to a backup folder and symlinks are created
        to the correct files path
        """

        if os.path.exists("files/" + key):
            print colors.blue("[NOTICE]") + " backing up: %s" % key

            new_dir = "backup/" + key
            helpers.make_and_move_to_dir(origin, new_dir)

            helpers.create_symlink(origin, "files/" + key)
        else:
            new_dir = "files/" + key
            helpers.make_and_move_to_dir(origin, new_dir)

            helpers.create_symlink(origin, new_dir)

    return True


def init():
    """
    This function will initialize the backup and files folder
    """

    dotconfig = helpers.create_config_file()

    if dotconfig is not True:
        return dotconfig

    current_directory = os.getcwd()
    helpers.set_dot_path(current_directory)

    if not os.path.exists("backup"):
        print colors.blue("[NOTICE]") + " creating backup folder"
        os.mkdir("backup")
        f = open('backup/.gitignore', 'w')
        f.write('# Ignore everything in this directory\n*\n\
            # Except this file\n!.gitignore')
        f.close()
    else:
        print colors.blue("[NOTICE]") + " backup folder found."

    if not os.path.exists("files"):
        print colors.blue("[NOTICE]") + " creating files folder"
        os.mkdir("files")
        open("files/.gitkeep", "w").close()
    else:
        print colors.blue("[NOTICE]") + " files folder found."


def add(args):
    """
    This will add a file or folder that needs to be tracked in the
    scribconfig file
    """
    helpers.check_args(args, 2)

    name = args[0]
    path = args[1]

    if not os.path.exists(path):
        sys.exit(colors.red("[ERROR]") + " file does not exist or file path"
                 " is not in the correct format")

    data = helpers.get_dotconfig()

    for k, v in data['files'].iteritems():
        if path == v:
            sys.exit(
                colors.blue("[NOTICE]") +
                            "the file %s is already being tracked" % path)

    data['files'].update({name: path})

    helpers.set_dotconfig(data)

    print colors.blue("[NOTICE]") + \
                      " %s added to the .dotconfig file, run 'dot' to symlink\
                       the files" % name


def remove(args):
    """
    This will remove a file or folder that needs to be untracked from the
    .dotconfig file and reset the files or folders to the prior destination
    """
    helpers.check_args(args, 1)

    name = args[0]
    data = helpers.get_dotconfig()

    dst = data['files'][name]
    src_dir = helpers.get_dot_path() + "/files/" + name + "/"
    src = helpers.get_dot_path() + "/files/" + name + "/" + os.path.basename(dst)

    # Set the file back in the correct location
    try:
        os.unlink(dst)              # remove symlink first
        shutil.move(src, dst)       # move source to symlink location
        shutil.rmtree(src_dir)      # remove source folder
    except IOError:
        sys.exit(colors.yellow("[ERROR]") + " not able to find file")

    # Remove reference from .dotconfig
    if name in data['files']:
        del data['files'][name]
    else:
        sys.exit(colors.yellow("[ERROR]") +
            " not able to find file in .dotconfig. Use 'dot list' to see the"
            " files")

    helpers.set_dotconfig(data)

    print colors.blue("[NOTICE]") + \
        " %s removed from .dotconfig file and moved to prior destination" \
        % name


def show_list():
    """
    This will list all the entries that are currently present in the
    .dotconfig file
    """
    data = helpers.get_dotconfig()

    if data['files']:
        print colors.red("***") + \
            colors.green(" The following files are being tracked ") + \
            colors.red("***")

        for k, v in data['files'].iteritems():
            print colors.red(k), colors.blue(v)
    else:
        print colors.blue("[NOTICE]") + "No files are being tracked, add " \
            "them with 'dot add'"
