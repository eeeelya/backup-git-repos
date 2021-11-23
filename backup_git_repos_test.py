import json
import stat
import unittest
import io
import yaml
import os
import errno
from pyfakefs.fake_filesystem_unittest import TestCase

import backup_git_repos

try:
    import unittest.mock as mock
except ImportError:
    import mock


class BackupGitReposTest(TestCase):
    config_data = {
        "save_path": "/home/eeeelya/Desktop/backup",
        "repos": ["git@github.com:eeeelya/backup-git-repos.git",
                  "git@github.com:course-4/meteo-centre.git"]
    }

    def setUp(self):
        self.setUpPyfakefs()

        with io.open("config.yaml", mode="wt") as stream_out:
            yaml.dump(self.config_data, stream_out)

    def tearDown(self):
        if os.path.exists("config.yaml"):
            self.fs.remove_object("config.yaml")

    def test_get_settings_from_config(self):
        with io.open("config.yaml", mode="rt") as stream_out:
            settings = yaml.safe_load(stream_out)

        # with mock.patch("backup_git_repos.open") as open_mock:

        self.assertEqual(settings, backup_git_repos._get_settings_from_config())


if __name__ == "__main__":
    unittest.main()
