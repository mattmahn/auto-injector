#!/usr/bin/env python3
"""Automatically renames CCDC inject PDFs based on their content"""

import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Dict

INJECT_COMPETITON_RE = re.compile(r'Competition:\s+(.+)')
INJECT_DURATION_RE = re.compile(
    r'Duration:\s+(?P<time>(?P<duration>\d+)\s+(?P<unit>.+))')
INJECT_FROM_RE = re.compile(r'From:\s+(.+)')
INJECT_NUM_RE = re.compile(r'Inject Number:\s+(\d+)')
INJECT_SUBJECT_RE = re.compile(r'Subject:\s+(.+)')
INJECT_TO_RE = re.compile(r'To:\s+(.+)')

FILENAME_BLACKLIST_RE = re.compile(r'[\[/*"?\]>\\<:\|]')
TEMP_DIR = tempfile.mkdtemp(prefix='auto-injector-')


def clean_tmp_dir():
    """Delete the temporary working directory and all files in it."""
    shutil.rmtree(TEMP_DIR)


def pdf_to_text(pdf_glob: str) -> Dict[str, str]:
    """
    Convert the PDF files specified by ``pdf_glob`` and returns a dictionary
    mapping the PDF filename to the text file output.
    """
    txt_files = dict()
    for filename in glob.iglob(pdf_glob):
        txt_file = os.path.join(TEMP_DIR, os.path.basename(filename) + '.txt')
        txt_files[filename] = txt_file
        subprocess.run(['pdftotext', filename, txt_file])
    return txt_files


def rename_pdfs(txt_files: Dict[str, str]):
    """Rename the original PDF files to their new name."""
    for pdf, txt in txt_files.items():
        with open(txt, 'r') as txt_file:
            content = txt_file.read()
            number = int(INJECT_NUM_RE.search(content)[1])
            subject = INJECT_SUBJECT_RE.search(content)[1]
        new_filename = '{num:03d} {subj}.pdf'.format(
            num=number, subj=subject)
        new_filename = FILENAME_BLACKLIST_RE.sub('', new_filename)
        os.replace(pdf, get_sibling_path(pdf, new_filename))


def get_sibling_path(path: str, filename: str) -> str:
    """Return a path to ``filename`` that is a sibling of ``path``."""
    return os.path.join(os.path.dirname(path), filename)


if __name__ == '__main__':
    rename_pdfs(pdf_to_text(sys.argv[1]))
    clean_tmp_dir()
