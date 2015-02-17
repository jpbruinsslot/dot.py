import os
import sys
import json
import shutil
import tempfile
from StringIO import StringIO

from nose.tools import *
from mock import patch

from dot import helpers


class TestCaseHelpers():

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

    def test_make_and_move_to_dir(self):
        """
        Test make_and_move_to_dir()

        It should move a file (in this case origin) to the specified location.
        When new_dir doesn't exist it should create a new dir and move the
        origin in it.
        """
        tempdir = tempfile.mkdtemp()
        os.chdir(tempdir)

        origin = open('testfile', 'w')
        origin.close()

        new_dir = "Riker"

        helpers.make_and_move_to_dir('testfile', new_dir)
        assert_true(os.path.exists(new_dir))
        assert_true(os.path.exists(new_dir + '/testfile'))

        shutil.rmtree(tempdir)

    def test_make_and_move_dir_new_dir_exists(self):
        """
        Test make_and_move_to_dir() when the new folder exists

        It should move a file (in this case origin) to the specified location.
        When new_dir exists it should move the origin in that dir.
        """
        tempdir = tempfile.mkdtemp()
        os.chdir(tempdir)

        origin = open('testfile', 'w')
        origin.close()

        new_dir = tempfile.mkdtemp()

        helpers.make_and_move_to_dir('testfile', new_dir)
        assert_true(os.path.exists(new_dir + '/testfile'))

        shutil.rmtree(tempdir)

    @patch('os.path.exists')
    def test_make_and_move_to_dir_file_not_found(self, mock_exists):
        """
        Test make_and_move_to_dir() when file is not found

        When trying to move a file to a file to a dir and the file doesn't
        exist it should return a SystemExit and an error message
        """
        origin = "Data"
        new_dir = "Spot"

        with assert_raises(SystemExit) as cm:
            helpers.make_and_move_to_dir(origin, new_dir)
        assert_in("not able to find file", cm.exception.args[0])

    def test_create_symlink(self):
        """
        Test create_symlink()

        Making a symlink should work as intended, origin is not yet created
        and will have the name of the tempfile that needs to be created.
        Structure is as follows:

        tempdir
        |
        |--tempdir2
        |  |-src
        |
        |-origin

        """

        tempdir = tempfile.mkdtemp()
        tempdir2 = tempfile.mkdtemp(dir=tempdir)
        src = tempfile.NamedTemporaryFile(dir=tempdir2)
        origin = tempdir + "/" + os.path.basename(src.name)

        helpers.create_symlink(origin, tempdir2)
        assert_true(os.path.islink(origin))

        src.close()
        shutil.rmtree(tempdir)

    def test_create_symlink_file_exists(self):
        """
        Test create_symlink() when file already exists

        When symlinking a file that already exists, e.g. trying to make a
        symlink in the same dir as the source file. It should raise a
        SystemExit and an error message.
        """
        tempdir = tempfile.mkdtemp()
        src = tempfile.NamedTemporaryFile(dir=tempdir)
        origin = tempdir + "/" + os.path.basename(src.name)

        with assert_raises(SystemExit) as cm:
            helpers.create_symlink(origin, tempdir)
        assert_in("symlinking failed, file exists", cm.exception.args[0])

        src.close()
        shutil.rmtree(tempdir)

    def test_check_args_pass(self):
        """
        Test check_args() when it passes

        The function should return true if the list of arguments is the same as
        expected.
        """
        args = ["dotconfig", "/home/erroneousboat/.dotconfig"]
        assert_true(helpers.check_args(args, 2))

    def test_check_args_fail(self):
        """
        Test check_args() when it fails

        When the length of the arguments is not the same as expected it should
        return a SystemExit and an error message
        """
        args = [
            "dotconfig", "/home/erroneousboat/.dotconfig", "USS Enterprise"]
        with assert_raises(SystemExit) as cm:
            helpers.check_args(args, 2)
        assert_in("incorrect number of arguments", cm.exception.args[0])

    def test_get_dotconfig(self):
        """
        Test get_dotconfig() when it passes

        When there is a dotconfig file it should not raise any errors
        """
        assert_true(helpers.get_dotconfig(path=self.tempfile_tracking.name))

    def test_get_dotconfig_no_data_file(self):
        """
        Test get_dotconfig() when there is no donfig file

        When there is no dotconfig file it should raise a SystemExit and
        display an error message
        """
        with assert_raises(SystemExit) as cm:
            helpers.get_dotconfig(path="/Q/Continuum/")
        assert_in("not able to find data file", cm.exception.args[0])

    def test_get_dotconfig_parse_failure(self):
        """
        Test get_dotconfig() when parsing of the file fails

        When the data in the datafile is not parseable it should catch a
        ValueError, raise a SystemError and display an error message
        """
        data = """ USS Stargazer """
        data_file = tempfile.NamedTemporaryFile()
        data_file.write(data)
        data_file.flush()

        with assert_raises(SystemExit) as cm:
            helpers.get_dotconfig(path=data_file.name)
        assert_in("not able to parse data file", cm.exception.args[0])

    def test_set_dotconfig(self):
        """
        Test set_dotconfig() when it passes

        Set dotconfig writes to the .dotconfig file. Make sure that changes
        are persisted.
        """
        data = "To boldy go, where no one has gone before."
        helpers.set_dotconfig(data, path=self.tempfile_non_tracking.name)
        self.tempfile_non_tracking.seek(0)  # read data from file
        assert_in("To boldy go, where no one has gone before.",
                  self.tempfile_non_tracking.read())

    def test_set_dotconfig_failed(self):
        """
        Test set_dotconfig() when it fails

        When it is not possible to write to the file, e.g. a wrong file path.
        It should raise a SystemExit and display an error message.
        """
        with assert_raises(SystemExit) as cm:
            helpers.set_dotconfig("Lore", path='doctor/noonien/soong/')
        assert_in("not able to write to data file", cm.exception.args[0])

    @patch('dot.helpers.get_dotconfig')
    def test_get_dot_path(self, mock_get_dotconfig):
        """
        Test get_dot_path() when it passes

        It should return the dot_path from the json file
        """
        data = json.loads(self.dotconfig_tracking)
        mock_get_dotconfig.return_value = data
        assert_equal(
            helpers.get_dot_path(),
            os.path.expanduser("~") + "/path/to/dotfiles/location")

    @patch('dot.helpers.get_dotconfig')
    def test_get_dot_path_empty(self, mock_get_dotconfig):
        """
        Test get_dot_path() when it's empty

        When the function can't find the path in the config file it should
        raise a SystemExit and display an error message
        """
        data = json.loads(self.dotconfig_non_tracking)
        mock_get_dotconfig.return_value = data

        with assert_raises(SystemExit) as cm:
            helpers.get_dot_path()
        assert_in("path not found in config file", cm.exception.args[0])

    @patch('dot.helpers.get_dotconfig')
    @patch('dot.helpers.set_dotconfig')
    def test_set_dot_path(self, mock_get_dotconfig, mock_set_dotconfig):
        """
        Test set_dot_path() when it passes

        It should set the correct path to the dotfiles and render a success
        message
        """
        data = json.loads(self.dotconfig_non_tracking)
        mock_get_dotconfig.return_value = data

        helpers.set_dot_path('path/to/dot/files')

        assert_in("set path/to/dot/files", self.output.getvalue())
