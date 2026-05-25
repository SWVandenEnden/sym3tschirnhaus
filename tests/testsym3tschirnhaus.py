#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Test Tschirnhaus transformation

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

from datetime import datetime

import sym3tschirnhaus
import symexpress3

testData = [ # 1
             { 'startFormula'    : 'x^4 - 94 x^2 - 480 x - 671'
             , 'eliminatePowers' : 2
             , 'variable'        : 'x'
             , 'depressed'       : 'x1^^4 + x1 * 198604800 * (1/103823) + (-169791667200) * (1/4879681) + x1 * 10^^(1/2) * i * (-159298560) * (1/103823) + 10^^(1/2) * i * (-13536460800) * (1/4879681)'
             , 'reversed'        : 'x1 + (-1) * x^^2 + 47 + (360/47) * x + (24/47) * x * 10^^(1/2) * i'
             },
             # 2
             { 'startFormula'    : 'y^3 + y^2 + y + 1'
             , 'eliminatePowers' : 2
             , 'variable'        : 'y'
             , 'depressed'       : '(20/27) + y1 * (2/3) + y1^^3'
             , 'reversed'        : 'y1 + (-1) * y + (-1/3)'
             },
             # 3   (x+1)(x+3)(x+5)(x+7)
             { 'startFormula'    : 'x^^4 + x^^3 * 16 + x^^2 * 86 + x * 176 + 105'
             , 'eliminatePowers' : 2
             , 'variable'        : 'x'
             , 'depressed'       : 'x2^^4 + x2 * (1024/5) + (21504/25)'
             , 'reversed'        : 'x2 + (-1) * x1^^2 + (4/5) * x1 * 5^^(1/2) * i + 5'
             }
           ]

startTime = datetime.now()

# test Tschirnhaus transformation
iTests = 0
iGood  = 0
iBad   = 0

clsTschirnhaus = sym3tschirnhaus.Sym3Tschirnhaus()

for dData in testData :
  iTests += 1
  print( f"Test: {iTests}", end='\r')

  clsTschirnhaus.startFormula     = dData.get( 'startFormula'    )
  clsTschirnhaus.eliminatePowers  = dData.get( 'eliminatePowers' )
  clsTschirnhaus.powerVariable    = dData.get( 'variable'        )

  clsTschirnhaus.calcTschirnhausTransformation()

  clsDepressed = symexpress3.SymFormulaParser( dData.get( 'depressed' ) )
  clsReversed  = symexpress3.SymFormulaParser( dData.get( 'reversed'  ) )

  clsDepressed.optimizeNormal()
  clsReversed.optimizeNormal()

  if not clsDepressed.isEqual( clsTschirnhaus.getFormulaDepressed() ) :
    iBad += 1

    print( f'Entry depressed {iTests} not equal'  )
    print( f'{clsTschirnhaus.getFormulaDepressed()}, expected: {clsDepressed}' )

  elif not clsReversed.isEqual( clsTschirnhaus.getFormulaReversed() ) :
    iBad += 1

    print( f'Entry reversed {iTests} not equal'  )
    print( f'{clsTschirnhaus.getFormulaReversed()}, expected: {clsReversed}' )
  else:
    iGood += 1

endTime   = datetime.now()
timeInSec = ( endTime - startTime ).total_seconds()

print( f"Number of tests: {iTests}, passed: {iGood}, failed; {iBad}, total time: {timeInSec} (sec)" )
