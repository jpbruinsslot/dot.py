import os
import sys
import json
import shutil
import tempfile
from StringIO import StringIO

from nose.tools import *
from mock import patch

from dot import main


class TestCaseMain():

    def setup(self):
        """
        To capture the output in the console for testing, redirect stdout
        during the unittest.
        See: http://stackoverflow.com/a/5975668/1346257
        """
        self.output = StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

        """
        Creating the test dotconfig files
        """
        self.dotconfig_tracking = """
        {
            "files" : { "testfile": "path/to/testfile"},
            "dot_path" : "/path/to/dotfiles/location"
        }
        """

        self.dotconfig_non_tracking = """
        {
            "files" : {},
            "dot_path" : ""
        }
        """

        self.tempfile_tracking = tempfile.NamedTemporaryFile(
            dir=os.path.expanduser("~"))
        self.tempfile_tracking.write(json.dumps(self.dotconfig_tracking,
                                                sort_keys=True, indent=4))
        self.tempfile_tracking.flush()

        self.tempfile_non_tracking = tempfile.NamedTemporaryFile(
            dir=os.path.expanduser("~"))
        self.tempfile_non_tracking.write(
            json.dumps(self.dotconfig_non_tracking,
                       sort_keys=True, indent=4))
        self.tempfile_non_tracking.flush()

    def teardown(self):
        self.output.close()
        sys.stdout = self.saved_stdout

        self.tempfile_tracking.close()
        self.tempfile_non_tracking.close()

    def test_command_not_known(self):
        """
        Test command not known

        Running a command not known to the program will exit it
        """
        with assert_raises(SystemExit):
            main.run_command("Warp 8", "Engage!")

    @patch('os.path.exists')
    def test_command_run(self, mock_exists):
        """
        Test command 'run'

        When running the command run without arguments it should run the run
        method and because we don't have a backup folder it should raise a
        system
        """
        mock_exists.return_value = False
        with assert_raises(SystemExit) as cm:
            main.run_command(None, None)
        assert_in("no backup and/or files folder found", cm.exception.args[0])

    @patch('os.getcwd')
    @patch('os.path.exists')
    @patch('dot.helpers.create_config_file')
    @patch('dot.helpers.set_dot_path')
    def test_command_init_dir_exists(self, mock_getcwd, mock_exists,
                                     mock_create_config_file,
                                     mock_set_dot_path):
        """
        Test command 'init' with a directory that exists

        When the back up folder and the files folder exist it should give
        notice to the user.
        """
        mock_create_config_file.return_value = True
        mock_set_dot_path.return_value = os.getcwd()
        mock_exists.return_value = True

        main.run_command("init", "")
        assert_in("found", self.output.getvalue())

    @patch('dot.helpers.create_config_file')
    @patch('dot.helpers.set_dot_path')
    def test_command_init_dir_nonexistent(self, mock_create_config_file,
                                          mock_set_dot_path):
        """
        Test command 'init' with non-existent directory

        When the back up folder and the files folder are not found it should
        be created. We need to make a temp dir in order to let the backup and
        files folder be created.
        """
        mock_create_config_file.return_value = True
        mock_set_dot_path.return_value = True

        tempdir = tempfile.mkdtemp()
        os.chdir(tempdir)
        main.run_command("init", "")

        assert_true(os.path.exists("backup"))
        assert_true(os.path.exists("files"))

        shutil.rmtree(tempdir)

    @patch('dot.helpers.get_dotconfig')
    @patch('dot.helpers.set_dotconfig')
    def test_command_add(self, mock_get_dotconfig, mock_set_dotconfig):
        """
        Test command 'add'

        Command add should run correctly given the right arguments
        """
        mock_get_dotconfig.return_value = self.dotconfig_tracking

        args = ["tempfile", self.tempfile_tracking.name]
        main.run_command("add", args)
        assert_in("added to the .dotconfig file", self.output.getvalue())

    def test_command_add_file_does_not_exists(self):
        """
        Test command 'add' when file doesn't exists

        When file path leads to a file that doesn't exist, then raise a
        SystemExit and display an error message
        """
        args = ["tempfile", "/to/wrong/path"]
        with assert_raises(SystemExit) as cm:
            main.add(args)
        assert_in("file does not exist", cm.exception.args[0])

    @patch('os.path.exists')
    @patch('dot.helpers.get_dotconfig')
    @patch('dot.helpers.set_dotconfig')
    def test_command_add_file_is_already_tracked(self, mock_exists,
                                                 mock_get_dotconfig,
                                                 mock_set_dotconfig):
        """
        Test command 'add' when the file is already being tracked

        When the file that is going to be added, is already being tracked in
        the .dotconfig file. Than raise a SystemExit exception and display an
        error message
        """
        data = json.loads(self.dotconfig_tracking)
        mock_get_dotconfig.return_value = data

        args = ["tempfile", "path/to/testfile"]
        with assert_raises(SystemExit) as cm:
            main.add(args)
        assert_in("is already being tracked", cm.exception.args[0])

    def test_command_remove(self):
        """
        TODO
        """
        # make folders
        # make symlink
        # excute remove
        pass

    def test_command_remove_file_not_found_on_system(self):
        """
        TODO
        """
        pass

    def test_command_remove_file_not_found_in_dotconfig(self):
        """
        TODO
        """
        pass

    @patch('dot.helpers.check_backup_and_files_folders')
    @patch('dot.helpers.get_dotconfig')
    @patch('dot.helpers.make_and_move_to_dir')
    @patch('dot.helpers.create_symlink')
    def test_command_run_from_main(self,
                                   mock_get_backup_and_files_folders,
                                   mock_get_dotconfig,
                                   mock_make_and_move_dir,
                                   mock_create_symlink):
        """
        Test command 'run' from main.py

        Running the run command (with path exists) should print out the notice
        that it's backing up files in the backup folder
        """
        mock_get_backup_and_files_folders.return_value = True

        data = json.loads(self.dotconfig_tracking)
        mock_get_dotconfig.return_value = data

        assert_true(main.run())

    @patch('os.path.exists')
    def test_command_run_missing_backup_and_files_folder(
            self, mock_exists):
        """
        Test command 'run' when backup folder is missing

        When running the run command and the backup folder is missing, it
        should raise a SystemExit and display a message.
        """
        mock_exists.return_value = False

        with assert_raises(SystemExit) as cm:
            main.run()
        assert_in("no backup and/or files folder found", cm.exception.args[0])

    @patch('dot.helpers.get_dotconfig')
    def test_command_list_tracked_files(self, mock_get_dotconfig):
        """
        Test command 'list' when files are being tracked

        Running the list command should return a list of files that are being
        tracked. Given that the config files is present and files are being
        tracked.
        """
        data = json.loads(self.dotconfig_tracking)
        mock_get_dotconfig.return_value = data

        main.run_command("list", "")
        assert_in(
            "The following files are being tracked", self.output.getvalue())

    @patch('dot.helpers.get_dotconfig')
    def test_command_list_no_tracked_files(self, mock_get_dotconfig):
        """
        Test command 'list' when files aren't being tracked

        Running the list command should return a message that no files are
        being tracked when the dotconfig file is empty
        """
        data = json.loads(self.dotconfig_non_tracking)
        mock_get_dotconfig.return_value = data

        main.run_command("list", "")
        assert_in("No files are being tracked, add them with 'dot add'",
                  self.output.getvalue())
