"""The command line drives the gate and the renderer against a ledger root."""

import contextlib
import io
from pathlib import Path
import unittest

from hogledger import cli

ROOT = Path(__file__).resolve().parent.parent


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(["--root", str(ROOT), *args])
    return code, out.getvalue(), err.getvalue()


class CommandLineTests(unittest.TestCase):
    def test_named_record_is_verified_alone(self):
        code, out, _ = run("verify", "sat-c6-n15")
        self.assertEqual(code, 0)
        self.assertEqual([line for line in out.splitlines() if line.startswith("[")],
                         [next(line for line in out.splitlines() if line.startswith("[OK] sat-c6-n15:"))])

    def test_unknown_record_id_fails(self):
        code, _, err = run("verify", "no-such-record")
        self.assertEqual(code, 1)
        self.assertIn("no-such-record", err)

    def test_registry_error_is_reported_not_raised(self):
        code, _, err = run("--root", "/nonexistent", "verify")
        self.assertEqual(code, 1)
        self.assertIn("REGISTRY ERROR", err)

    def test_render_check_exits_zero_when_current(self):
        self.assertEqual(run("render", "--check")[0], 0)

    def test_unknown_arguments_are_rejected(self):
        with self.assertRaises(SystemExit) as raised, contextlib.redirect_stderr(io.StringIO()):
            cli.main(["render", "--bogus"])
        self.assertEqual(raised.exception.code, 2)

    def test_a_command_is_required(self):
        with self.assertRaises(SystemExit) as raised, contextlib.redirect_stderr(io.StringIO()):
            cli.main([])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
