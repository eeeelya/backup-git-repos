import unittest
import io
import yaml
import os
from pyfakefs.fake_filesystem_unittest import TestCase

import backup_git_repos

try:
    import unittest.mock as mock
except ImportError:
    import mock


class BackupGitReposTest(TestCase):
    save_path = "/tmp/backup"
    config_path = "/tmp"
    
    config_data = {
        "save_path": "",
        "repos": []
    }
    # Set the main path to the location of a fake python interpreter.
    # python_path = "/usr/bin/python3"

    def setUp(self):
        self.setUpPyfakefs()

        # The provided path to python interpreter is to exist and be accessible to an active user.
        # self.fs.create_file(self.python_path)

        self.fs.create_dir(self.save_path)

        # Create fake python kernels to run tests without damage to the current operating system.
        with io.open(os.path.join(self.save_path, "config.yaml"), mode="wt") as stream_out:
            # Create a new config on the current machine.
            yaml.dump(self.config_data, stream_out)

    def tearDown(self):
        if os.path.exists(self.save_path):
            # Remove all repositories from current machine.
            self.fs.remove_object(self.save_path)


if __name__ == "__main__":
    unittest.main()
