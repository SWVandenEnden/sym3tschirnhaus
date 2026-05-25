#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Command line interface

    Copyright (C) 2026 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sym3tschirnhaus
import symexpress3


def CalcSolution( polyString, polyVar, powerElim, outputFormat ):
  """
  Do the Tschirnhaus transformation
  """
  if len( polyString ) == 0:
    print( "No parameters are given, nothing to do" )
    return

  # default output format, solutions as string and calculated values
  if outputFormat in( "", None ):
    outputFormat = "s"

  try:

    clsTschirnhaus = sym3tschirnhaus.Sym3Tschirnhaus()
    output   = None

    # set variables
    # pylint: disable=multiple-statements
    if powerElim != None: clsTschirnhaus.eliminatePowers = powerElim
    if polyVar   != None: clsTschirnhaus.variable        = polyVar

    clsTschirnhaus.startFormula  = polyString

    if 'h' in outputFormat:
      output = symexpress3.SymToHtml( None, "Tschirnhaus transformation" )
      clsTschirnhaus.htmlOutput = output

    # calculate the solutions
    clsTschirnhaus.calcTschirnhausTransformation()

    # output data
    for cOutput in outputFormat:
      if cOutput == "s":

        print( "Tschirnhaus transformation" )
        for iLevel in range( 0, clsTschirnhaus.numberOfTransformations ):
          print( f"Level {iLevel}: {clsTschirnhaus.getFormulaDepressed(iLevel)}" )
          print( f"Reversed formula: {clsTschirnhaus.getFormulaReversed(iLevel)}" )

      elif cOutput == "h":
        pass # do nothing html (output) is already set

      else:
        print( f"Unknown output format '{cOutput}' ignored" )

    if output != None:
      output.closeFile()
      output = None

  except Exception as exceptAll: # pylint: disable=broad-exception-caught
    print( f"Error: {str( exceptAll )}" )



def DisplayVersion():
  """
  Display version information
  """
  print( "Version    : " + sym3tschirnhaus.__version__    )

  print( "Author     : " + sym3tschirnhaus.__author__     )
  print( "Copyright  : " + sym3tschirnhaus.__copyright__  )
  print( "License    : " + sym3tschirnhaus.__license__    )
  print( "Maintainer : " + sym3tschirnhaus.__maintainer__ )
  print( "Email      : " + sym3tschirnhaus.__email__      )
  print( "Status     : " + sym3tschirnhaus.__status__     )


def DisplayHelp():
  """
  Display help
  """
  print( "Do the Tschirnhaus transformation of a given polynomial" )
  print( " " )
  print( "usage: python -m sym3tschirnhaus [options] [arg]" )
  print( "options: " )
  print( "  -h           : Help" )
  print( "  -v           : Version information" )
  print( "  -o <format>  : Output format" )
  print( "                 s - string format (default)" )
  print( "                 h - html" )
  print( "  -s           : Maximum number of powers to eliminate, default is 2" )
  print( "  -d           : Variable polynomial, default is 'x'" )
  print( "arg: <symexpress3 string>" )
  print( " " )
  print( "Example: " )
  print( 'python -m sym3tschirnhaus "2 x^^4 + 3 x^^3 + 4 x^^2 + 5 x^^1 + 6"' )
  print( 'python -m sym3tschirnhaus -o s -s 1 -d x "2 x^^4 + 3 x^^3 + 4 x^^2 + 5 x^^1 + 6"' )

def CommandLine( argv ):
  """
  Process the command line parameters
  """
  outputFormat = ""
  polyString   = ""
  powerElim    = None  # number of powers to eliminate
  polyVar      = None  # variable in polynomial

  nrarg = len( argv )

  # nothing given, then display help
  if nrarg <= 1:
    DisplayHelp()

  mode = ""
  for iCnt in range( 1, nrarg ) :
    cArg = argv[ iCnt ]

    if mode == "output":
      outputFormat = cArg
      mode = ""
      continue

    if mode == "elim":
      powerElim = int( cArg )
      mode = ""
      continue

    if mode == "variable":
      polyVar = cArg
      mode = ""
      continue


    if cArg == "-h" :
      DisplayHelp()
      return  # direct stop by help

    if cArg == "-v" :
      DisplayVersion()
      return  # direct stop by version information

    # pylint: disable=multiple-statements
    if   cArg == "-o": mode = "output"
    elif cArg == "-s": mode = "elim"
    elif cArg == "-d": mode = "variable"

    else:
      if cArg.startswith( "-" ):
        print( f"Unknown option: {cArg}, use -h for help")
      else:
        # collect arguments
        polyString = cArg

  CalcSolution( polyString, polyVar, powerElim, outputFormat )


# ---------------------------
# The end
# ---------------------------
