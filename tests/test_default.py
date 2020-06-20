import unittest

import click
from click.testing import CliRunner

from click_constrained_option import ConstrainedOption


class TestDefault(unittest.TestCase):
    def test_default_func(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, default_func=lambda a: a[::-1])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=123"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '123', 'b': '321'}, eval(result.output))

        result = runner.invoke(cli, ["--a=123", "--b=123"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '123', 'b': '123'}, eval(result.output))


if __name__ == '__main__':
    unittest.main()
