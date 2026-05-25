# Python Tschirnhaus transformation module

A Python module for the Tschirnhaus transformation

## Usage

### Do the Tschirnhaus transformation
The solutions is a symexpress3 object
```py
>>> import sym3tschirnhaus
>>> objTschirnhaus = sym3tschirnhaus.Sym3Tschirnhaus()
>>> objTschirnhaus.startFormula = "2 x^^4 + 3 x^^3 + 4 x^^2 + 5 x^^1 + 6"
>>> objTschirnhaus.calcTschirnhausTransformation()
>>> print( f"Tschirnhaus transformation: {objTschirnhaus.getFormulaDepressed()}\n" )
Tschirnhaus transformation: 4 * x2^^4 + x2 * (4388530/50653) + (4252423075/29986576) + x2 * (5/2)^^(1/2) * (-383565/50653) + (5/2)^^(1/2) * (-49204155/1874161)
```

### Options
Options for the Tschirnhaus transformation
```py
>>> import sym3tschirnhaus
>>> objTschirnhaus = sym3tschirnhaus.Sym3Tschirnhaus()
>>> objTschirnhaus.steps = 2
>>> objTschirnhaus.variable = "x"
>>> objTschirnhaus.startFormula = "2 x^^4 + 3 x^^3 + 4 x^^2 + 5 x^^1 + 6"
>>> objTschirnhaus.calcTschirnhausTransformation()
>>> for iIndex in range( 0, objTschirnhaus.numberOfTransformations): print( f"Depressed: {objTschirnhaus.getFormulaDepressed(iIndex)}, reversed: {objTschirnhaus.getFormulaReversed(iIndex)}")
Depressed: (9357/2048) + 2 * x1^^4 + x1^^2 * (37/16) + x1 * (91/32), reversed: x1 + (-1) * x + (-3/8)
Depressed: 4 * x2^^4 + x2 * (4388530/50653) + (4252423075/29986576) + x2 * (5/2)^^(1/2) * (-383565/50653) + (5/2)^^(1/2) * (-49204155/1874161), reversed: x2 + (-1) * x1^^2 + (-37/64) + (273/148) * x1 + (-4/37) * x1 * (5/2)^^(1/2)
```

### Command line
python -m sym3tschirnhaus

- *Help*: python -m sym3tschirnhaus -h
- *Tschirnhaus transformation*: python -m sym3tschirnhaus "2 x^^4 + 3 x^^3 + 4 x^^2 + 5 x^^1 + 6"

### Graphical user interface
https://github.com/SWVandenEnden/websym3
