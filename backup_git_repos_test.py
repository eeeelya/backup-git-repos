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
    config_path = "."

    def setUp(self):
        self.setUpPyfakefs()

        # self.fs.create_dir()

        with io.open("config.yaml", mode="wt") as stream_out:
            yaml.dump(self.config_data, stream_out)

    def tearDown(self):
        if os.path.exists("config.yaml"):
            self.fs.remove_object("config.yaml")

    def test_get_settings_from_config(self):
        with mock.patch("backup_git_repos.open") as open_mock:
            open_mock.side_effect = OSError(errno.EPERM, "")
            backup_git_repos._get_settings_from_config(self.config_path)

    def test_get_save_path(self):
        self.assertEqual(self.config_data["save_path"], backup_git_repos._get_save_path())

    def test_get_repos_list(self):
        self.assertEqual(self.config_data["repos"], backup_git_repos._get_repos_list())

    @mock.patch("backup_git_repos._logger")
    def test_get_repos_list_error(self, logger_mock):
        with self.assertRaises(SystemExit) as system_exit:
            self.assertEqual(self.config_data["repos"], backup_git_repos._get_repos_list())

            logger_mock.error.assert_called_with(
                "There are no repositories."
            )

            self.assertEqual(system_exit.exception.code, 0)

    @mock.patch("backup_git_repos.git.Git")
    @mock.patch("backup_git_repos.shutil.move")
    @mock.patch("backup_git_repos.shutil.rmtree")
    @mock.patch("backup_git_repos.tempfile.TemporaryDirectory")
    @mock.patch("backup_git_repos.os.listdir")
    def test_clone_repos(self, mock_listdir, mock_temp_dir, mock_rmtree, mock_move, mock_git):

        backup_git_repos.clone_repos(self.config_data["save_path"])
        # mock_git.assert_called_with(self.save_path)
        # mock_move.assert_called_with()
        # mock_rmtree.assert_called_with()

    @mock.patch("backup_git_repos.git.Git")
    @mock.patch("backup_git_repos._logger")
    @mock.patch("backup_git_repos.os.listdir")
    @mock.patch("backup_git_repos.tempfile.TemporaryDirectory")
    def test_clone_repos_error(self, mock_temp_dir, mock_listdir, mock_git, logger_mock):
        mock_listdir.side_effect = OSError(errno.ENOENT, "")

        with self.assertRaises(SystemExit) as system_exit:
            backup_git_repos.clone_repos(self.config_data["save_path"])

            logger_mock.error.assert_called_with(
                "List of repositories is empty!"
            )

            self.assertEqual(system_exit.exception.code, 0)

    def test_calculate_hash_for_file(self):
        # Надо передать путь и файл, а где их взять?
        # И как вообще можно протестировать функцию, которая просто считает хэш для файлов
        # backup_git_repos._calculate_hash_for_file()
        pass

    @mock.patch("backup_git_repos.os.listdir")
    def test_get_files_with_hash(self, mock_listdir):
        # mock_listdir.side_effect = OSError(errno.ENOENT, "")
        backup_git_repos.get_files_with_hash(self.config_data["save_path"])
        # self.assertTrue(os.path.isfile(os.path.join(self.config_data["save_path"], "meteo-centre.zip")))

    @mock.patch("backup_git_repos.os.listdir")
    def test_archive_repos(self, mock_listdir):
        # и тут...
        backup_git_repos.archive_repos(self.config_data["save_path"])


if __name__ == "__main__":
    unittest.main()
