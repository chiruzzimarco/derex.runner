from compose.cli.main import main
from derex.runner.docker import ensure_volumes_present
from derex.runner.plugins import Registry
from derex.runner.plugins import setup_plugin_manager
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

import click
import derex
import hashlib
import os
import pkg_resources
import re
import sys
import yaml


def run_compose(
    args: List[str],
    variant: str = "services",
    dry_run: bool = False,
    project: Optional["derex.runner.project.Project"] = None,
):
    """Run a docker-compose command passed in the `args` list.
    If `variant` is passed, load plugins for that variant.
    If a project is passed, load plugins for that project.
    """
    plugin_manager = setup_plugin_manager()
    registry = Registry()
    if project:
        for opts in plugin_manager.hook.local_compose_options(project=project):
            registry.add(
                key=opts["name"], value=opts["options"], location=opts["priority"]
            )
    else:
        ensure_volumes_present()
        for opts in plugin_manager.hook.compose_options():
            if opts["variant"] == variant:
                registry.add(
                    key=opts["name"], value=opts["options"], location=opts["priority"]
                )
    settings = [el for lst in registry for el in lst]
    old_argv = sys.argv
    try:
        sys.argv = ["docker-compose"] + settings + args
        if not dry_run:
            click.echo(f'Running {" ".join(sys.argv)}')
            main()
        else:
            click.echo("Would have run:")
            click.echo(click.style(" ".join(sys.argv), fg="blue"))
    finally:
        sys.argv = old_argv
