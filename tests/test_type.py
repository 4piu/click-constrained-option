import unittest

import click
from click.testing import CliRunner

from click_constrained_option import ConstrainedOption


class TestType(unittest.TestCase):
    def test_type_func(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, type_func=lambda a: click.INT if a == '0' else click.STRING)
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=1", "--b=str"])
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '1', 'b': 'str'}, eval(result.output))

        result = runner.invoke(cli, ["--a=0", "--b=str"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid value for '--b'", result.output)


if __name__ == '__main__':
    unittest.main()
