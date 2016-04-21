#!/usr/bin/env python
import os, sys
import argparse
import textwrap

from pydoc_markdown import write_module, import_module
from pydoc_markdown.markdown import MarkdownWriter
parser = argparse.ArgumentParser(
    prog='pydoc-markdown',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
        Simple (ie. quick and dirty) script to generate a Markdown
        formatted help on a Python module. Contributions are welcome.
        Project Homepage:  https://github.com/NiklasRosenstein/pydoc-markdown
        ''')
)

writer = MarkdownWriter(file('ss.md', 'w'))
from liyuoa_pm import settings
for m in settings.INSTALLED_APPS:
    if m.find('django') == 0:
        continue
    print m
    module = import_module(m)
    write_module(writer, module)
writer.fp.close()