import unittest
from unittest.mock import patch, mock_open, call, MagicMock
from manage_requirements_files.cli import (
    pip_freeze,
    read_requirements,
    write_requirements,
    update_requirements,
    main,
)


class TestPipFreeze(unittest.TestCase):
    @patch("manage_requirements_files.cli.subprocess.check_output")
    def test_pip_freeze_normal_output(self, mock_check_output):
        # Mocking the subprocess output to simulate pip freeze
        mock_check_output.return_value = "package1==1.0\npackage2==2.0"
        expected_output = {"package1==1.0", "package2==2.0"}
        result = pip_freeze()
        self.assertEqual(result, expected_output)

    @patch("manage_requirements_files.cli.subprocess.check_output")
    def test_pip_freeze_empty_output(self, mock_check_output):
        # Testing with no packages installed
        mock_check_output.return_value = ""
        expected_output = set()
        result = pip_freeze()
        self.assertEqual(result, expected_output)

    @patch("manage_requirements_files.cli.subprocess.check_output")
    def test_pip_freeze_raises_exception(self, mock_check_output):
        # Testing how your function handles subprocess exceptions
        mock_check_output.side_effect = Exception("An error occurred")
        with self.assertRaises(Exception):
            pip_freeze()


class TestReadRequirements(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="package1>=1.0\npackage2\n\n",
    )
    def test_read_existing_file(self, mock_file):
        # Test reading from an existing file
        expected_output = {"package1>=1.0", "package2"}
        result = read_requirements("requirements.txt")
        self.assertEqual(result, expected_output)
        mock_file.assert_called_once_with("requirements.txt", "r")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_read_empty_file(self, mock_file):
        # Test reading an empty file
        expected_output = set()
        result = read_requirements("requirements.txt")
        self.assertEqual(result, expected_output)
        mock_file.assert_called_once_with("requirements.txt", "r")

    @patch(
        "builtins.open",
        side_effect=[
            FileNotFoundError(),
            mock_open(read_data="").return_value,
        ],
    )
    def test_file_creation_on_not_found(self, mock_file):
        # Test handling of FileNotFoundError and file creation if not present
        expected_output = set()
        result = read_requirements("requirements.txt")
        self.assertEqual(result, expected_output)
        self.assertEqual(
            mock_file.call_args_list[0], call("requirements.txt", "r")
        )
        self.assertEqual(
            mock_file.call_args_list[1], call("requirements.txt", "a")
        )


class TestWriteRequirements(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_existing_file(self, mock_file):
        # Test appending new lines to an existing file
        new_lines = ["django>=3.2", "requests>=2.25"]
        write_requirements("requirements.txt", new_lines)
        mock_file.assert_called_once_with("requirements.txt", "a")
        mock_file().write.assert_has_calls(
            [call("django>=3.2\n"), call("requests>=2.25\n")]
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_new_file(self, mock_file):
        # Test writing to a new file
        new_lines = ["flask>=1.1"]
        write_requirements("new_requirements.txt", new_lines)
        mock_file.assert_called_once_with("new_requirements.txt", "a")
        mock_file().write.assert_called_once_with("flask>=1.1\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_write_multiple_lines(self, mock_file):
        # Test writing multiple lines to the file
        new_lines = ["fastapi>=0.65", "uvicorn>=0.14"]
        write_requirements("requirements.txt", new_lines)
        mock_file.assert_called_once_with("requirements.txt", "a")
        calls = [call(line + "\n") for line in new_lines]
        mock_file().write.assert_has_calls(calls)


class TestUpdateRequirements(unittest.TestCase):
    @patch("manage_requirements_files.cli.print")
    @patch("manage_requirements_files.cli.write_requirements")
    @patch("manage_requirements_files.cli.read_requirements")
    @patch("manage_requirements_files.cli.pip_freeze")
    def test_with_new_dependencies(
        self,
        mock_pip_freeze,
        mock_read_requirements,
        mock_write_requirements,
        mock_print,
    ):
        mock_pip_freeze.return_value = {"django>=3.2", "requests>=2.25"}
        mock_read_requirements.side_effect = [
            {"django>=3.2"},  # Existing dependencies in target_file
            {"flask>=1.1"},  # Existing dependencies in other_file
        ]

        update_requirements(
            "target_requirements.txt", "other_requirements.txt"
        )

        mock_write_requirements.assert_called_once_with(
            "target_requirements.txt", {"requests>=2.25"}
        )
        mock_print.assert_called_once_with(
            "Updated target_requirements.txt with new dependencies: "
            + "{'requests>=2.25'}"
        )

    @patch("manage_requirements_files.cli.print")
    @patch("manage_requirements_files.cli.write_requirements")
    @patch("manage_requirements_files.cli.read_requirements")
    @patch("manage_requirements_files.cli.pip_freeze")
    def test_without_new_dependencies(
        self,
        mock_pip_freeze,
        mock_read_requirements,
        mock_write_requirements,
        mock_print,
    ):
        mock_pip_freeze.return_value = {"django>=3.2"}
        mock_read_requirements.side_effect = [
            {"django>=3.2"},  # Existing dependencies in target_file
            {"flask>=1.1"},  # Existing dependencies in other_file
        ]

        update_requirements(
            "target_requirements.txt", "other_requirements.txt"
        )

        mock_write_requirements.assert_not_called()
        mock_print.assert_called_once_with(
            "No new dependencies to add to target_requirements.txt."
        )


class TestMainFunction(unittest.TestCase):
    @patch('manage_requirements_files.cli.update_requirements')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_prod_mode(self, mock_parse_args, mock_update_requirements):
        # Setup mock to simulate command line arguments
        mock_parse_args.return_value = MagicMock(mode='prod')

        # Call main to test behavior
        main()

        # Check if update_requirements was called correctly
        mock_update_requirements.assert_called_once_with("requirements.txt", "requirements-dev.txt")

    @patch('manage_requirements_files.cli.update_requirements')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_dev_mode(self, mock_parse_args, mock_update_requirements):
        # Setup mock to simulate command line arguments
        mock_parse_args.return_value = MagicMock(mode='dev')

        # Call main to test behavior
        main()

        # Check if update_requirements was called correctly
        mock_update_requirements.assert_called_once_with("requirements-dev.txt", "requirements.txt")



if __name__ == "__main__":
    unittest.main()
