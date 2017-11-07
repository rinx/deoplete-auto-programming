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

    def _query_git(self, querystring):
        command = ['git', 'grep', '--fixed-string', '-h', '-E', '(^\s*|.*\s+)%s' % querystring]
        cands = subprocess.check_output(command).splitlines()
        return cands

    def gather_candidates(self, context):
        if not self.executable_git:
            return []

        querystring = context['complete_str']
        try:
            words = [
                    x.decode(context['encoding'])
                    for x in self._query_git(re.sub(r'^\s*', '', querystring))
                    ]
        except subprocess.CalledProcessError:
            return []

        words = [x[re.search(querystring, x).start():] for x in words]
        words = [re.sub(r'^\s*', '', x) for x in words]

        return [{ 'word': x } for x in words]
