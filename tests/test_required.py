import unittest

import click
from click.testing import CliRunner

from click_constrained_option import ConstrainedOption


class TestRequired(unittest.TestCase):
    def test_required_func(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, required_func=lambda a: a == '0')
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--b'", result.output)

    def test_required_if(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, required_if="a")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--b'", result.output)

    def test_required_if_not(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, required_if_not="a")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, [])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--b'", result.output)

    def test_required_if_all_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, required_if_all_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--b=1"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--c'", result.output)

    def test_required_if_none_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, required_if_none_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, [])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--c'", result.output)

    def test_required_if_any_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, required_if_any_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--c'", result.output)

    def test_required_if_one_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, required_if_one_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--c'", result.output)

    def test_composition(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c")
        @click.option("--d")
        @click.option("--e", cls=ConstrainedOption, required_if="a", required_if_not="b", required_if_one_of=["c", "d"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--c=1"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option '--e'", result.output)


if __name__ == '__main__':
    unittest.main()
