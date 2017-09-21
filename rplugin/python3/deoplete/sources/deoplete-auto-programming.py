from os.path import expanduser, expandvars
import re
import subprocess
from .base import Base

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'auto-programming'
        self.mark = '[auto-programming]'

        self.executable_git = self.vim.call('executable', 'git')

    def on_init(self, context):
        vars = context['vars']

        self.min_pattern_length = vars.get('deoplete#sources#auto-programming#min_pattern_length', 2)

        try:
            # init(load suorce) only work
            pass
        except Exception:
            # Ignore the error
            pass

    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    def _query_git(self, querystring):
        command = ['git', 'grep', '--fixed-string', '-h', '-e', querystring]
        return subprocess.check_output(command).splitlines()

    def gather_candidates(self, context):
        if not self.executable_git:
            return []

        try:
            words = [
                    x.decode(context['encoding'])
                    for x in self._query_git(context['complete_str'][:2])
                    ]
        except subprocess.CalledProcessError:
            return []

        return [{ 'word': x } for x in words]
