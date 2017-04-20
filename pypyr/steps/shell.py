"""pypyr Step that executes a shell as a sub-process.

The context['cmd'] string must be formatted exactly as it would be when typed
at the shell prompt. This includes, for example, quoting or backslash escaping
filenames with spaces in them. The shell defaults to /bin/sh.
"""
import pypyr.format.string
import pypyr.log.logger
import subprocess

# logger means the log level will be set correctly
logger = pypyr.log.logger.get_logger(__name__)


def run_step(context):
    """Run shell command without shell interpolation.

    Context is a dictionary or dictionary-like.
    Will execute context['cmd'] in the shell as a sub-process.
    The shell defaults to /bin/sh.
    The context['cmd'] string must be formatted exactly as it would be when
    typed at the shell prompt. This includes, for example, quoting or backslash
    escaping filenames with spaces in them.
    There is an exception to this: Escape curly braces: if you want a literal
    curly brace, double it like {{ or }}.

    context is mandatory. When you execute the pipeline, it should look
    something like this: pipeline-runner [name here] --context 'cmd=ls -a'.

    context['cmd'] will interpolate anything in curly braces for values
    found in context. So if your context looks like this:
        key1: value1
        key2: value2
        cmd: mything --arg1 {key1}

    The cmd passed to the shell will be "mything --arg value1"
    """
    logger.debug("started")
    assert context, ("context must be set for step shell. Did you set "
                     "--context 'cmd=<<shell cmd here>>'?")
    assert 'cmd' in context, ("context['cmd'] must exist for step shell.")

    # input string is a command like 'ls -l | grep boom'. Split into list on
    # spaces to allow for natural shell language input string.
    logger.debug(f"Executing command string: {context['cmd']}")

    interpolated_string = pypyr.format.string.get_interpolated_string(
        input_string=context['cmd'],
        context=context)
    logger.debug(f"Interpolated string: {interpolated_string}")

    # check=True throws CalledProcessError if exit code != 0
    subprocess.run(interpolated_string, shell=True, check=True)

    logger.debug("done")
