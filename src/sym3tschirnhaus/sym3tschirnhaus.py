#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Tschirnhaus transformation

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


    Based on: https://en.wikipedia.org/wiki/Tschirnhaus_transformation
              https://numbersandshapes.net/posts/tschirnhausens_transformations_quartic/


"""
import cubicequation
import sym3resultant
import symexpress3


class Sym3Tschirnhaus():
  """
  Do the Tschirnhaus transformation
  """

  def __init__( self ):
    # defaults
    self._powerVariable   = 'x'  # the power variable
    self._startFormula    = None # symexpress3 formula
    self._output          = None # symexpress3.SymToHtml object
    self._level           = {}   # internal level for each transformation
    self._maxdiffernt     = 2    # max different in power between hightest and second power. Other solutions are not supported
    self._eliminatePowers = 2    # set number of powers to eliminate

  @property
  def startFormula(self):
    """
    Symexpress3 formula
    """
    return self._startFormula

  @startFormula.setter
  def startFormula(self, val):
    self._startFormula = symexpress3.ConvertToSymexpress3String( val )


  @property
  def eliminatePowers(self):
    """
    Number of powers to eliminate
    """
    return self._eliminatePowers

  @eliminatePowers.setter
  def eliminatePowers(self, val):
    if not isinstance( val, int ):
      raise NameError( f'eliminatePowers is incorrect: {type(val)}, expected int object ' )

    # some defaults
    val = min( val, self._maxdiffernt )
    val = max( val, 1 )

    self._eliminatePowers = val


  @property
  def htmlOutput(self):
    """
    Set html output object
    """
    return self._output

  @htmlOutput.setter
  def htmlOutput(self, val):
    if val != None and ( not isinstance( val, symexpress3.SymToHtml )) :
      raise NameError( f'htmlOutput is incorrect: {type(val)}, expected SymToHtml object ' )
    self._output = val


  @property
  def powerVariable(self):
    """
    The power variable, default is x
    """
    return self._powerVariable

  @powerVariable.setter
  def powerVariable(self, val):
    if not isinstance( val, str ):
      raise NameError( f'powerVariable is incorrect: {type(val)}, expected str' )
    self._powerVariable = val


  @property
  def numberOfTransformations(self):
    """
    The number of transformations
    """
    return len( self._level )


  def getLevel( self, iLevel ):
    """
    Get the level object (transformation information). If None is given, highest level will be returned
    """
    if len( self._level ) == 0:
      return None

    if iLevel == None:
      iLevel = max( self._level )

    if iLevel in self._level:
      return self._level[ iLevel ]

    return None


  def getVariableStart( self, iLevel = None ):
    """
    Get the start (original) variable of the given level. If no level is given highest level is used
    """
    oLevel = self.getLevel( iLevel )
    if oLevel == None:
      return None
    return oLevel[ 'var' ]


  def getVariableNew( self, iLevel = None ):
    """
    Get the new (replaced) variable of the given level. If no level is given highest level is used
    """
    oLevel = self.getLevel( iLevel )
    if oLevel == None:
      return None
    return oLevel[ 'varNew' ]

  def getFormulaStart( self, iLevel = None ):
    """
    Get the start (original) formula of the given level. If no level is given highest level is used
    """
    oLevel = self.getLevel( iLevel )
    if oLevel == None:
      return None
    return oLevel[ 'formula' ].copy()

  def getFormulaDepressed( self, iLevel = None ):
    """
    Get the depressed formula of the given level. If no level is given highest level is used
    """
    oLevel = self.getLevel( iLevel )
    if oLevel == None:
      return None
    return oLevel[ 'depressedFormula' ].copy()


  def getFormulaReversed( self, iLevel = None ):
    """
    Get the reversed formula of the given level. If no level is given highest level is used
    This is a formula that equal's to zero. You can use solvePolynomial() to solve it after replace the new variable.
    """
    oLevel = self.getLevel( iLevel )
    if oLevel == None:
      return None
    return oLevel[ 'reversedFormula' ].copy()


  def solvePolynomial( self, oFormula, cVariable ):
    """
    Solve the given polynomial (example: a x^^3 + b x^^2 ...) for the given variable
    The result is always an array
    """
    if not isinstance( oFormula, symexpress3.SymExpress):
      raise NameError( f"solvePolynomial, oFormula is of type {type(oFormula)}, expected a SymExpress object")

    if not isinstance( cVariable, str):
      raise NameError( f"solvePolynomial, cVariable is of type {type(cVariable)}, expected a str object")

    result   = []
    coeff    = symexpress3.PolynomialCoefficients( oFormula, cVariable, True )
    maxPower = max( coeff )

    # print( f"Max power: {maxPower}")

    match maxPower:
      case 0 :
        # no x found, nothing to do
        result.append( coeff[0])

      case 1 :
        # a x + b -> x = -b / a
        valueStr = f" (-1 * ( {coeff[0]} ) ) / ({coeff[1]})"
        value    = symexpress3.SymFormulaParser( valueStr )
        value.optimizeNormal()
        result.append( value )

      case 2:
        # a x^^2 + b x + c -> quadratic formula

        # this gives a quadratic solved it
        frmABCstr = "(-b + (b^^2 - 4 * a * c)^(1/2)) / ( 2 * a )"
        frmABC    = symexpress3.SymFormulaParser( frmABCstr )
        dReplace = {}
        dReplace[ 'a' ] = str( coeff[2] )
        dReplace[ 'b' ] = str( coeff[1] )
        dReplace[ 'c' ] = str( coeff[0] )
        frmABC.replaceVariable( dReplace )

        # print( f"before frmABC: {str(frmABC)}")

        frmABC.optimizeExtended()

        # print( f"frmABC: {str(frmABC)}")
        # take value out of array
        if isinstance( frmABC.elements[ 0 ], symexpress3.SymArray ) :
          result.append( frmABC.elements[ 0 ].elements[0] )
          result.append( frmABC.elements[ 0 ].elements[1] )
        else:
          result.append( frmABC )

      case 3:
        # a x^^3 + b x^^2 + c x + d -> cubic formula

        objCubic = cubicequation.CubicEquation()
        objCubic.a = coeff[ 3 ]
        objCubic.b = coeff[ 2 ]
        objCubic.c = coeff[ 1 ]
        objCubic.d = coeff[ 0 ]

        objCubic.calcSolutions()

        result.append( objCubic.x1Optimized )
        result.append( objCubic.x2Optimized )
        result.append( objCubic.x3Optimized )

      case _ :
        raise NameError( f"solvePolynomial, formula has power {maxPower} and is not supported. ({str(oFormula)})")

    # print( "Result:")
    # for elem in result:
    #   print( str(elem))
    # print( "")

    return result


  #
  # Tschirnhaus transformation
  #
  def calcTschirnhausTransformation(self):
    """
    Do the Tschirnhaus transformation
    """

    def RaiseError( cError ):
      """
      Raise an error and put the message also in the output file if set
      """
      if self._output != None:
        self._output.writeLine( f'Error: {cError}' )
      raise NameError( cError )


    def SplitFormula( iLevel, cVar, oFormula ):
      """
      Split the formula in its coefficients
      """
      oLevel = {}

      oLevel[ 'var'    ] = cVar
      # oLevel[ 'newVar' ] = cVar + str( iLevel + 1)
      oLevel[ 'formula'] = oFormula

      if oFormula.power != 1:
        RaiseError( f"Formula has power {oFormula.power} but only 1 is allowed")

      if oFormula.symType != '+':
        RaiseError( f"Formula has type {oFormula.symType}. Excepted a '+' formula")

      if oFormula.numElements() <= 1 :
        RaiseError( f"Formula has {oFormula.numElements()} elements. Excepted at least 2 elements")

      # check of given variable exist in formula
      # sym3Var = symexpress3.SymVariable( self._powerVariable )

      dVars = oFormula.getVariables()
      if cVar not in dVars:
        RaiseError( f"Variable {cVar} does not exist in the formula ({str(oFormula)})")

      # if self._output != None:
      #   self._output.writeLine( f'Variable: {cVar}')
      #   self._output.writeLine( '')

      # get all the coefficients
      try:
        coeff = symexpress3.PolynomialCoefficients( oFormula, cVar )
      except Exception as err: # pylint: disable=broad-exception-caught
        RaiseError( str( err ) )

      highestKey = max( coeff )
      lowestKey  = min( coeff )
      secondKey  = lowestKey

      for key in coeff:
        if key == highestKey:
          continue
        secondKey = max( secondKey, key )


      oLevel[ 'coeff'      ] = coeff
      oLevel[ 'highestKey' ] = highestKey
      oLevel[ 'lowestKey'  ] = lowestKey
      oLevel[ 'secondKey'  ] = secondKey

      self._level[ iLevel ] = oLevel

    def CanDepressFormula( iLevel ):
      """
      Check of formula can be optimized
      """
      if self._eliminatePowers < iLevel:
        return False

      oLevel = self._level[ iLevel ]

      highestKey = oLevel[ 'highestKey' ]
      lowestKey  = oLevel[ 'lowestKey'  ]
      secondKey  = oLevel[ 'secondKey'  ]
      # coeff      = oLevel[ 'coeff'      ]
      # cVar       = oLevel[ 'var'        ]
      oFormula   = oLevel[ 'formula'    ]

      if highestKey < 3:
        RaiseError( f"Highest power found {highestKey}. Minimal power is 3. ({oFormula})")

      if lowestKey != 0:
        # RaiseError( f"Lowest power found {lowestKey}. Expected 0. ({oFormula})")
        return False

      if secondKey < 2 :
        return False
        # RaiseError( f"Replace power found {secondKey}. Expected 2 or higher. ({oFormula})")

      # max elimination reached
      if highestKey - secondKey > self._eliminatePowers :
        return False

      if highestKey - secondKey > self._maxdiffernt :
        if self._output != None:
          self._output.writeLine( f'Maximum different between highest and second power supported is {self._maxdiffernt}, found {highestKey - secondKey}')
        return False

      return True

    def CreateDepressedFormula( iLevel ):
      """
      Make depressed formula
      """
      oLevel = self._level[ iLevel ]

      highestKey        = oLevel[ 'highestKey' ]
      lowestKey         = oLevel[ 'lowestKey'  ]
      secondKey         = oLevel[ 'secondKey'  ]
      coeff             = oLevel[ 'coeff'      ]
      cVar              = oLevel[ 'var'        ]
      oFormula          = oLevel[ 'formula'    ]

      if self._output != None:
        self._output.writeLine( f'Level: {iLevel}')
        self._output.writeLine( '--------')
        self._output.writeSymExpressWithStr( oFormula )

        for key, value in coeff.items():
          cExtra = ''
          if highestKey == key:
            cExtra = ' ->  Highest power'

          if lowestKey == key:
            cExtra = ' ->  Lowest power'

          if secondKey == key:
            cExtra = ' ->  Replace power'

          self._output.writeLine( f'Power: {key}, Coefficient: {str( value) }{cExtra}')

        self._output.writeLine( '')


      # replace var
      varNew = self._powerVariable + str( iLevel + 1 )
      oLevel[ 'varNew' ] = varNew

      diffPower = highestKey - secondKey
      if diffPower == 1:

        # y = x + b/ ( a * highestpower )
        # -> y - x - b/ ( a * highestpower ) = 0
        # x = y - b/ ( a * highestpower )

        # 0 expressie als op reversed opgeven
        # power van expressie ook opslaan...
        # altijd een array van antwoorden teruggen als revered waarde wordt opgevraagd
        #


        # replace expression
        # this is only valid if highestKey and secondKey different 1 !!!!
        # newVar = a * x^^(diff) + b * x^^(diff-1) + c x^^(diff-2) ... until diff - ? is zero
        replaceExpression = f'{varNew} - ( ({str( coeff[secondKey] )} ) / ( ({str( coeff[highestKey])} ) * {highestKey}) )'

        oLevel[ 'replaceExpression' ] = replaceExpression

        reversedFormula  = f"{varNew} - {cVar} - ( ({str( coeff[secondKey] )} ) / ( ({str( coeff[highestKey])} ) * {highestKey}) )"
        oReversedFormula = symexpress3.SymFormulaParser( reversedFormula )
        oReversedFormula.optimizeNormal()

        oLevel[ 'reversedFormula' ] = oReversedFormula

        dReplace = {}
        dReplace[ cVar ] = replaceExpression
        fReplace = oFormula.copy()
        fReplace.replaceVariable( dReplace )
        fReplace.optimize()

        fReplace.optimizeNormal()

        if self._output != None:
          # self._output.writeLine( f'Replace formula: {str(fReplace)}' )
          self._output.writeSymExpressWithStr( fReplace, "Depressed formula")
          self._output.writeLine( f"New variable: {varNew}")

          self._output.writeSymExpressWithStr( oReversedFormula, f"Link between original variable {cVar} and new variable {varNew} (give zero)")
          self._output.writeLine( "")

      elif diffPower == 2:
        # y = x^^2 + r x + s
        varNewR = varNew + 'r'
        varNewS = varNew + 's'

        newExpress     = f'{varNew} = {cVar}^^2 + {varNewR} * {cVar} + {varNewS}'
        newExpressZero = f'{varNew} - {cVar}^^2 - {varNewR} * {cVar} - {varNewS}'

        if self._output != None:
          self._output.writeLine( f'New expression: {newExpress}')
          self._output.writeLine( f'New expression zero: {newExpressZero}')
          self._output.writeLine( '')
          # self._output.writeSymExpressWithStr( oFormula )

        # calculate the resultant
        objResultant = sym3resultant.Sym3Resultant()
        objResultant.variable = cVar
        objResultant.formula1 = oFormula
        objResultant.formula2 = newExpressZero
        objResultant.calcResultant()

        frmResultant = objResultant.resultant
        resCoef      = symexpress3.PolynomialCoefficients( frmResultant, varNew )

        if self._output != None:
          self._output.writeSymExpressWithStr( frmResultant, "Resultant" )
          for key, value in resCoef.items():
            self._output.writeLine( f'Power: {key}, Coefficient: {str( value) }')
          self._output.writeLine( '')

        # make the second highest power zero = highest power - 1
        powerSecond = resCoef[ highestKey - 1 ]

        valuePowerSecond = self.solvePolynomial( powerSecond, varNewS )

        if self._output != None:
          self._output.writeLine( f'{ highestKey - 1}th power of resultant for variable {varNewS}')
          self._output.writeSymExpressWithStr( powerSecond, varNewS )

          for key, value in enumerate( valuePowerSecond ):
            self._output.writeLine( f'Value {key} =  {str(value)}' )

          self._output.writeLine( '')

        # make the 2th power zero (for r) = highest power - 2
        powerThird = resCoef[ highestKey - 2  ]

        # replace s
        powerThirdReplace = powerThird.copy ()
        dReplace = {}
        dReplace[ varNewS ] = str( valuePowerSecond[0] )
        powerThirdReplace.replaceVariable( dReplace )
        powerThirdReplace.optimizeNormal()

        valuePowerThird = self.solvePolynomial( powerThirdReplace, varNewR )

        if self._output != None:
          self._output.writeSymExpressWithStr( powerThirdReplace, f"{ highestKey - 2}th power with {varNewS} replaced" )
          self._output.writeLine( f'{ highestKey - 2}th power of resultant for variable {varNewR}')

          for key, value in enumerate( valuePowerThird ):
            self._output.writeLine( f'Value {key} =  {str(value)}' )

          self._output.writeLine( '')
          self._output.writeSymExpressWithStr( valuePowerThird[0], f"{varNewR} value chosen" )

        # put r and s in the resultant
        dReplace = {}
        dReplace[ varNewR ] = str( valuePowerThird[0]  )
        dReplace[ varNewS ] = str( valuePowerSecond[0] )

        frmLight = frmResultant.copy()
        frmLight.replaceVariable( dReplace )
        frmLight.optimizeNormal()

        reversedFormula  = newExpressZero
        oReversedFormula = symexpress3.SymFormulaParser( reversedFormula )
        oReversedFormula.replaceVariable( dReplace )
        oReversedFormula.optimizeNormal()

        oLevel[ 'reversedFormula' ] = oReversedFormula

        if self._output != None:
          self._output.writeSymExpressWithStr( frmLight, "Depressed formula" )
          self._output.writeLine( f"New variable: {varNew}")

          self._output.writeSymExpressWithStr( oReversedFormula, f"Link between original variable {cVar} and new variable {varNew} (give zero)")
          self._output.writeLine( "")

        oLevel[ 'varNew' ] = varNew

        fReplace = frmLight

      else:
        RaiseError( f"Power different greater then 2 not supported ({diffPower})")

      oLevel[ 'depressedFormula' ] = fReplace

      SplitFormula( iLevel + 1, varNew, fReplace )


    self._level = {}

    if self._output != None:
      self._output.writeLine( 'Tschirnhaus transformation' )
      self._output.writeLine( 'Based on <a target="_blank" href="https://en.wikipedia.org/wiki/Tschirnhaus_transformation">https://en.wikipedia.org/wiki/Tschirnhaus_transformation</a>' )
      self._output.writeLine( '' )


    # get formula in symexpress3 format
    sym3Formula = symexpress3.SymFormulaParser( self._startFormula )

    # only principal root supported, so force it
    sym3Formula.optimize()
    sym3Formula.optimize( 'setOnlyOne')


    SplitFormula( 0, self._powerVariable, sym3Formula )

    iLevelCounter = 0
    while CanDepressFormula( iLevelCounter ):
      CreateDepressedFormula( iLevelCounter )
      iLevelCounter += 1

      # safety check
      if iLevelCounter >= self._level[ 0 ][ 'highestKey' ]:
        break

    # delete levels without reversedFormula because there is always 1 to many created
    iDelKey = -1
    for key, value in self._level.items():
      if 'reversedFormula' not in value:
        iDelKey = key
        break
    del self._level[ iDelKey ]

    # for key, value in self._level.items():
    #   print( f"key {key} {value}" )
