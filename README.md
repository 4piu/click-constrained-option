# click-constrained-option

[![PyPI version](https://badge.fury.io/py/click-constrained-option.svg)](https://badge.fury.io/py/click-constrained-option)
[![Build Status](https://travis-ci.org/nobody-65534/click-constrained-option.svg?branch=master)](https://travis-ci.org/nobody-65534/click-constrained-option)


**click-constrained-option** is an extension package that adds constrains to option in [Click](https://github.com/pallets/click/).

Tested under click 7.x

## What it does

Build option that: 
* mutually exclusive with others
* depend on other options
* is required conditionally
* is promoted conditionally
* set its default value conditionally
* set its type conditionally

## Quick start

```bash
pip install click-constrained-option
```

```python
# example.py

import click
from click_constrained_option import ConstrainedOption

@click.command()
@click.option(cls=ConstrainedOption,
              group_require_one=["apple", "orange", "pear"])
@click.option("--apple",
              cls=ConstrainedOption,
              is_flag=True)
@click.option("--orange",
              cls=ConstrainedOption,
              is_flag=True)
@click.option("--pear",
              cls=ConstrainedOption,
              is_flag=True)
def cli(**kwargs):
    click.echo(kwargs)


if __name__ == "__main__":
    cli()

```
```shell script
$ python example.py

Error: require exact one of '--apple' '--orange' '--pear'

$ python example.py --apple --pear

Error: require exact one of '--apple' '--orange' '--pear'
```

## API

|kwarg|type|usage|
|:---|:---|:---|
|allowed_func|`function`|return True to indicate allowance, vice versa
|allowed_if|`str`|name of the option
|allowed_if_not|`str`|name of the option
|allowed_if_all_of|`list`|list of the option names
|allowed_if_none_of|`list`|list of the option names
|allowed_if_any_of|`list`|list of the option names
|allowed_if_one_of|`list`|list of the option names
|required_func|`function`|return True to indicate requirement, vice versa
|required_if|`str`|name of the option
|required_if_not|`str`|name of the option
|required_if_all_of|`list`|list of the option names
|required_if_none_of|`list`|list of the option names
|required_if_any_of|`list`|list of the option names
|required_if_one_of|`list`|list of the option names
|prompt_func|`function`|return True to indicate prompt, vice versa
|prompt_if|`str`|name of the option
|prompt_if_not|`str`|name of the option
|prompt_if_all_of|`list`|list of the option names
|prompt_if_none_of|`list`|list of the option names
|prompt_if_any_of|`list`|list of the option names
|prompt_if_one_of|`list`|list of the option names
|group_require_one|`list`|list of the option names
|group_require_any|`list`|list of the option names
|group_require_all|`list`|list of the option names
|default_func|`function`|return a value to use as the default
|type_func|`function`|return a valid type of the option

### Note

* If multiple kwargs are used, then all of them must be satisfied. For example, if `prompt_if` and `prompt_if_all_of` are specified, then the option is prompted only when both condition hold true.  

* If the custom function has an argument equals an option name in the command, then the value of that option will be used as argument. For example, value of `--foo` will be passed to a custom function `bar(foo)`. 

## Examples

### Dependency and exclusive relation

`--username` is allowed if `--login` is set:
```python
import click
from click_constrained_option import ConstrainedOption

@click.command()
@click.option("--username",
              cls=ConstrainedOption,
              allowed_if="login")
@click.option("--login", is_flag=True)
def cli(**kwargs):
    click.echo(kwargs)


if __name__ == "__main__":
    cli()
```
```shell script
$ python example.py --username=foo

Error: Usage for '--username': require '--login'
```

`--login` is allowed if at least one of `--userid` and `--email` is specified, and `--oauth` is not set:
```python
import click
from click_constrained_option import ConstrainedOption

@click.command()
@click.option("--login",
              cls=ConstrainedOption,
              is_flag=True,
              allowed_if_any_of=["userid", "email"],
              allowed_if_not="cookie")
@click.option("--userid")
@click.option("--email")
@click.option("--oauth", is_flag=True)
def cli(**kwargs):
    click.echo(kwargs)


if __name__ == "__main__":
    cli()
```
```shell script
$ python example.py --login --userid=foo --oauth

Error: Usage for '--login': conflict with '--oauth'

$ python example.py --login

Error: Usage for '--login': require at least one of '--userid' '--email'
```

`--port` is required if `--listen` is an IP address:
```python
import click
import re
from click_constrained_option import ConstrainedOption

@click.command()
@click.option("--port",
              cls=ConstrainedOption,
              required_func=lambda b: re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", b))
@click.option("--listen")
def cli(**kwargs):
    click.echo(kwargs)


if __name__ == "__main__":
    cli()
```
```shell script
$ python example.py --listen=127.0.0.1

Error: Missing option '--port'
```

### Mutually exclusive group

Exact one of the `--order-by-date` `--order-by-name` `--order-by-rank` must be set:
```python
import click
from click_constrained_option import ConstrainedOption

@click.option(cls=ConstrainedOption,
              group_require_one=["order_by_name", "order_by_rank", "order_by_date"])
@click.option("--order-by-name",
              cls=ConstrainedOption,
              is_flag=True)
@click.option("--order-by-rank",
              cls=ConstrainedOption,
              is_flag=True)
@click.option("--order-by-date",
              cls=ConstrainedOption,
              is_flag=True)
def cli(**kwargs):
    click.echo(kwargs)


if __name__ == "__main__":
    cli()
```
```shell script
$ python example.py

Error: require exact one of '--order-by-name' '--order-by-rank' '--order-by-date'
```

### Conditional prompt

`--password` will be prompted if one of `--userid` `--email` is specified

```python
import click
from click_constrained_option import ConstrainedOption

@click.command()
@click.option("--userid")
@click.option("--email")
@click.option("--password", 
              hide_input=True,
              prompt_if_one_of=["userid", "email"])
def cli(**kwargs):
    click.echo(kwargs)


if __name__ == "__main__":
    cli()
```
```shell script
$ python example.py --userid

Password: 
```

### Conditional type

Type of `--time` will be int if `--time-format=timestamp`

```python
import click
from click_constrained_option import ConstrainedOption

@click.command()
@click.option("--time-format",
              type=click.Choice(["iso-8601", "timestamp"]))
@click.option("--time",
              cls=ConstrainedOption,
              type_func=lambda time_format: click.INT if time_format == "timestamp" else click.STRING)
def cli(**kwargs):
    click.echo(kwargs)


if __name__ == "__main__":
    cli()
```

```shell script
$ python --time-format="timestamp" --time=str_not_int

Error: Invalid value for '--time': str_not_int is not a valid integer
```

### Conditional default

Default of `--lucky` is set through custom function

```python
import click
from click_constrained_option import ConstrainedOption
from random import randint

@click.command()
@click.option("--lucky",
              default=lambda : randint(0, 9))
def cli(**kwargs):
    click.echo(kwargs)


if __name__ == "__main__":
    cli()
```

```shell script
$ python example.py

{'lucky': '5'}
```