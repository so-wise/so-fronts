"""Tests for plotting-adjacent scripts."""
import os
import tempfile
import unittest
from unittest.mock import patch

import src.move_figures as mov


class TestPlotScripts(unittest.TestCase):
    """Unit tests for figure moving command generation."""

    def test_move_builds_expected_copy_commands(self):
        """move should issue one copy command per expected figure."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            figure_root = os.path.join(tmp_dir, "figures")
            image_root = os.path.join(tmp_dir, "images")
            with patch.object(mov.cst, "FIGURE_PATH", figure_root):
                with patch.object(mov.cst, "FINAL_LOC", image_root):
                    with patch.object(mov.os, "system", return_value=0) as system_mock:
                        mov.move(copy_command="cp")

        self.assertEqual(system_mock.call_count, 14)
        commands = [call.args[0] for call in system_mock.call_args_list]
        self.assertTrue(all(command.startswith("cp ") for command in commands))
        self.assertTrue(any("figure-1.png" in command for command in commands))
        self.assertTrue(any("figure-B2.png" in command for command in commands))

    def test_move_respects_copy_command_argument(self):
        """Caller-provided copy_command should be used verbatim."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch.object(mov.cst, "FIGURE_PATH", os.path.join(tmp_dir, "figs")):
                with patch.object(mov.cst, "FINAL_LOC", os.path.join(tmp_dir, "out")):
                    with patch.object(mov.os, "system", return_value=0) as system_mock:
                        mov.move(copy_command="mv")

        commands = [call.args[0] for call in system_mock.call_args_list]
        self.assertTrue(commands)
        self.assertTrue(all(command.startswith("mv ") for command in commands))


suite = unittest.TestLoader().loadTestsFromTestCase(TestPlotScripts)
