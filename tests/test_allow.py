import unittest

import click
from click.testing import CliRunner

from click_constrained_option import ConstrainedOption


class TestAllow(unittest.TestCase):
    def test_allowed_func(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, allowed_func=lambda a: a == '0')
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--b=1"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': '1'}, eval(result.output))

        result = runner.invoke(cli, ["--a=1", "--b=1"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("validation failed", result.output)

    def test_allowed_if(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, allowed_if="a")
        @click.option("--c")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--b=1"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': '1', 'c': None}, eval(result.output))

        result = runner.invoke(cli, ["--b=0", "--c=1"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("require '--a'", result.output)

    def test_allowed_if_not(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, allowed_if_not="a")
        @click.option("--c")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--b=0", "--c=1"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': None, 'b': '0', 'c': '1'}, eval(result.output))

        result = runner.invoke(cli, ["--a=0", "--b=1"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("conflict with '--a'", result.output)

    def test_allowed_if_all_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, allowed_if_all_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--b=1", "--c=2"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': '1', 'c': '2'}, eval(result.output))

        result = runner.invoke(cli, ["--a=0", "--c=1"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("require all of '--a' '--b'", result.output)

    def test_allowed_if_none_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, allowed_if_none_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--c=0"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': None, 'b': None, 'c': '0'}, eval(result.output))

        result = runner.invoke(cli, ["--a=0", "--c=1"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("conflict with '--a' '--b'", result.output)

    def test_allowed_if_any_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, allowed_if_any_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--c=1"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': None, 'c': '1'}, eval(result.output))

        result = runner.invoke(cli, ["--c=0"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("require at least one of '--a' '--b'", result.output)

    def test_allowed_if_one_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, allowed_if_one_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--c=1"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': None, 'c': '1'}, eval(result.output))

        result = runner.invoke(cli, ["--a=0", "--b=1", "--c=2"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("require exact one of '--a' '--b'", result.output)

        result = runner.invoke(cli, ["--c=0"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("require exact one of '--a' '--b'", result.output)

    def test_composition(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c")
        @click.option("--d")
        @click.option("--e", cls=ConstrainedOption, allowed_if="a", allowed_if_not="b", allowed_if_one_of=["c", "d"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--c=1", "--e=2"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': None, 'c': '1', 'd': None, 'e': '2'}, eval(result.output))

        result = runner.invoke(cli, ["--a=0", "--b=1", "--e=2"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("conflict with '--b'", result.output)


if __name__ == '__main__':
    unittest.main()
