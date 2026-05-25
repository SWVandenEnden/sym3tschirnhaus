# pylint: disable=invalid-name
"""
Command line handling
"""

import sys

if __name__ == '__main__':
  from sym3tschirnhaus import tschirnhauscmd
  tschirnhauscmd.CommandLine( sys.argv )
