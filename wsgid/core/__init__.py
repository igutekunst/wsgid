#encoding: utf-8

__all__ = ['StartResponse', 'StartResponseCalledTwice', 'Plugin', 'run_command', 'get_main_logger', 'validate_input_params']

import sys
import logging
import plugnplay
from command import ICommand
import parser
from wsgidapp import WsgidApp
import re
import os

Plugin = plugnplay.Plugin


class StartResponse(object):

    def __init__(self):
        self.headers = []
        self.status = ''
        self.body = ''
        self.called = False
        self.body_written = False

    def __call__(self, status, response_headers, exec_info=None):
        if self.called and not exec_info:
            raise StartResponseCalledTwice()

        if exec_info and self.body_written:
            try:
                raise exec_info[0], exec_info[1], exec_info[2]
            finally:
                exec_info = None  # Avoid circular reference (PEP-333)

        self.headers = response_headers
        self.status = status

        self.called = True
        return self._write

    def _write(self, body):
        self.body_written = True
        self.body += body


class StartResponseCalledTwice(Exception):
    pass


log = logging.getLogger('wsgid')


def get_main_logger():
    return log


def set_main_logger(logger):
    log = logger


def run_command():
    '''
    Extract the first command line argument (if it exists)
    and tries to find a ICommand implementor for it.
    If found, run it. If not does nothing.
    '''
    command_implementors = ICommand.implementors()
    if command_implementors and len(sys.argv) > 1:
        cname = sys.argv[1]  # get the command name
        for command in command_implementors:
            if command.name_matches(cname):
                # Remove the command name, since it's not defined
                # in the parser options
                sys.argv.remove(cname)
                command.run(parser.parse_options(use_config=False), command_name=cname)
                return True
    return False


ZMQ_SOCKET_SPEC = re.compile("(?P<proto>inproc|ipc|tcp|pgm|epgm)://(?P<address>.*)$")
TCP_SOCKET_SPEC = re.compile("(?P<adress>.*):(?P<port>[0-9]+)")

def _is_valid_socket(sockspec):
    generic_match = ZMQ_SOCKET_SPEC.match(sockspec)
    if generic_match:
        proto = generic_match.group('proto')
        if proto == "tcp":
            return TCP_SOCKET_SPEC.match(generic_match.group('address'))
        else:
            return True
    return False

def validate_input_params(app_path=None, recv=None, send=None):
    if app_path and not os.path.exists(app_path):
        raise Exception("path {0} does not exist.\n".format(app_path))
    if not recv or not _is_valid_socket(recv):
        raise Exception("Recv socket is mandatory, value received: {0}\n".format(recv))
    if not send or not _is_valid_socket(send):
        raise Exception("Send socker is mandatory, value received: {0}\n".format(send))


from wsgid import Wsgid
