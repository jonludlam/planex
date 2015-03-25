#!/usr/bin/env python

# Some generic utils used by several other files

import subprocess
import os
import pipes
import tempfile
import yum
import logging


def load_mock_config(cfg):
    """
    Load the yum configuration from the mock configuration file
    Nasty, but this is how mock loads its configuration file...
    From /usr/sbin/mock
    """

    import mockbuild.util  # pylint: disable=F0401
    unpriv_uid = os.getuid()
    version = 1
    pkgpythondir = mockbuild.__path__[0]
    config_opts = mockbuild.util.setup_default_config_opts(
        unpriv_uid, version, pkgpythondir)
    config_opts['config_paths'] = []
    config_opts['config_paths'].append(cfg)
    execfile(cfg)
    return config_opts


def get_yumbase(config):
    """
    Initialise the Yum library and return an object which can be
    used to query the package database
    """
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(config['yum.conf'])
        temp.flush()

        yumbase = yum.YumBase()
        yumbase.repos.disableRepo('*')
        yumbase.getReposFromConfigFile(temp.name)

    return yumbase


def run(cmd, check=True, env=None, inputtext=None):
    """
    Run a command, dumping it cut-n-pasteably if required. Checks the return
    code unless check=False. Returns a dictionary of stdout, stderr and return
    code (rc)
    """
    logging.debug("running command: %s",
                  (" ".join([pipes.quote(word) for word in cmd])))

    if env is None:
        env = os.environ.copy()

    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    [stdout, stderr] = proc.communicate(inputtext)

    if check and proc.returncode != 0:
        logging.error("command failed: %s",
                      (" ".join([pipes.quote(word) for word in cmd])))
        logging.error("stdout: %s", stdout)
        logging.error("stderr: %s", stderr)
        raise Exception

    return {"stdout": stdout, "stderr": stderr, "rc": proc.returncode}