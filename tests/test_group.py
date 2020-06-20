import unittest

import click
from click.testing import CliRunner

from click_constrained_option import ConstrainedOption


class TestGroup(unittest.TestCase):
    def test_group_require_one(self):
        @click.command()
        @click.option(
            cls=ConstrainedOption,
            group_require_one=["a", "b"])
        @click.option("--a")
        @click.option("--b")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': None}, eval(result.output))

        result = runner.invoke(cli, ["--a=0", "--b=1"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("require exact one of '--a' '--b'", result.output)

    def test_group_require_any(self):
        @click.command()
        @click.option(
            cls=ConstrainedOption,
            group_require_any=["a", "b"])
        @click.option("--a")
        @click.option("--b")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': None}, eval(result.output))

        result = runner.invoke(cli, [])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("require at least one of '--a' '--b'", result.output)

    def test_group_require_all(self):
        @click.command()
        @click.option(
            cls=ConstrainedOption,
            group_require_all=["a", "b"])
        @click.option("--a")
        @click.option("--b")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--b=1"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': '1'}, eval(result.output))

        result = runner.invoke(cli, ["--a=0"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("require all of '--a' '--b'", result.output)


if __name__ == '__main__':
    unittest.main()
