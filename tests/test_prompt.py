import re
import unittest

import click
from click.testing import CliRunner

from click_constrained_option import ConstrainedOption


class TestPrompt(unittest.TestCase):
    def test_prompt_func(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, prompt_func=lambda a: a == '0')
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"], input="1\n")
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': '1'}, eval(re.findall(r".+", result.output)[-1]))

    def test_prompt_if(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, prompt_if="a")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"], input="1\n")
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': '1'}, eval(re.findall(r".+", result.output)[-1]))

    def test_prompt_if_not(self):
        @click.command()
        @click.option("--a")
        @click.option("--b", cls=ConstrainedOption, prompt_if_not="a")
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, [], input="0\n")
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': None, 'b': '0'}, eval(re.findall(r".+", result.output)[-1]))

    def test_prompt_if_all_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, prompt_if_all_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--b=1"], input="3\n")
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': '1', 'c': '3'}, eval(re.findall(r".+", result.output)[-1]))

    def test_prompt_if_none_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, prompt_if_none_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, [], input="0\n")
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': None, 'b': None, 'c': '0'}, eval(re.findall(r".+", result.output)[-1]))

    def test_prompt_if_any_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, prompt_if_any_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"], input="1\n")
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': None, 'c': '1'}, eval(re.findall(r".+", result.output)[-1]))

    def test_prompt_if_one_of(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c", cls=ConstrainedOption, prompt_if_one_of=["a", "b"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0"], input="1\n")
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': None, 'c': '1'}, eval(re.findall(r".+", result.output)[-1]))

    def test_composition(self):
        @click.command()
        @click.option("--a")
        @click.option("--b")
        @click.option("--c")
        @click.option("--d")
        @click.option("--e", cls=ConstrainedOption, prompt_if="a", prompt_if_not="b", prompt_if_one_of=["c", "d"])
        def cli(**kwargs):
            click.echo(kwargs)

        runner = CliRunner()

        result = runner.invoke(cli, ["--a=0", "--c=1"], input="2\n")
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual({'a': '0', 'b': None, 'c': '1', 'd': None, 'e': '2'}, eval(re.findall(r".+", result.output)[-1]))


if __name__ == '__main__':
    unittest.main()
