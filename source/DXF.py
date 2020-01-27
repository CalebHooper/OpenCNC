import ezdxf

# Angle Units
DECIMAL_DEGREES = 0
GRAD = 2
RADIANS = 3

# Length Units
UNITLESS = 0
INCHES = 1
FEET = 2
MILES = 3
MILI_METERS = 4
CENTI_METERS = 5
METERS = 6
KILO_METERS = 7
MICRO_INCHES = 8
MILS = 9
YARD = 10
ANGSTROMS = 11
NANO_METERS = 12
MICRONS = 13
DECI_METERS = 14
DECA_METERS = 15
HECTO_METERS = 16
GIGA_METERS = 17
ASTRONOMICAL_UNIT = 18
LIGHT_YEAR = 19
PARSECS = 20
US_SURVEY_FEET = 21
US_SURVEY_INCH = 22
US_SURVEY_YARD = 23
US_SURVEY_MILE = 24

# ----- Conversion -----
def convertToMeter(fromUnit, val):

    if fromUnit == UNITLESS:
        return val
    
    if fromUnit == INCHES or US_SURVEY_INCH:
        return val * .0254

    if fromUnit == FEET or US_SURVEY_FEET:
        return val * .3048

    if fromUnit == MILES or US_SURVEY_MILE:
        return val * 1609.34

    if fromUnit == MILI_METERS:
        return val * .001

    if fromUnit == CENTI_METERS:
        return val * .01

    if fromUnit == METERS:
        return val

    if fromUnit == KILO_METERS:
        return val * 1000

    if fromUnit == MICRO_INCHES:
        return val * .0000000254

    if fromUnit == MILS:
        return val * .0000254

    if fromUnit == YARD or US_SURVEY_YARD:
        return val * .9144

    if fromUnit == ANGSTROMS:
        return val * .0000000001

    if fromUnit == NANO_METERS:
        return val * .000000001

    if fromUnit == MICRONS:
        return val * .000006

    if fromUnit == DECI_METERS:
        return val * .1

    if fromUnit == DECA_METERS:
        return val * 10

    if fromUnit == HECTO_METERS:
        return val * 100

    if fromUnit == GIGA_METERS:
        return val * 1000000000.0

    if fromUnit == ASTRONOMICAL_UNIT:
        return val * 149600000000.0

    if fromUnit == LIGHT_YEAR:
        return val * 9461000000000000.0

    if fromUnit == PARSECS:
        return val * 30860000000000000.0

def convertFromMeter(toUnit, val):

    if toUnit == UNITLESS:
        return val
    
    if toUnit == INCHES or US_SURVEY_INCH:
        return val * 39.3701

    if toUnit == FEET or US_SURVEY_FEET:
        return val * 3.28084

    if toUnit == MILES or US_SURVEY_MILE:
        return val * 0.000621371

    if toUnit == MILI_METERS:
        return val * 1000.0

    if toUnit == CENTI_METERS:
        return val * 100.0

    if toUnit == METERS:
        return val

    if toUnit == KILO_METERS:
        return val * .001

    if toUnit == MICRO_INCHES:
        return val * 39370078.74

    if toUnit == MILS:
        return val * 39370.1

    if toUnit == YARD or US_SURVEY_YARD:
        return val * 1.09361

    if toUnit == ANGSTROMS:
        return val * 10000000000.0

    if toUnit == NANO_METERS:
        return val * 1000000000.0

    if toUnit == MICRONS:
        return val * 1000000.0

    if toUnit == DECI_METERS:
        return val * 10

    if toUnit == DECA_METERS:
        return val * .1

    if toUnit == HECTO_METERS:
        return val * .01

    if toUnit == GIGA_METERS:
        return val * .000000009

    if toUnit == ASTRONOMICAL_UNIT:
        return val * .000000000006684

    if toUnit == LIGHT_YEAR:
        return val * .0000000000000001057

    if toUnit == PARSECS:
        return val * .00000000000000003241

def normalize(fromUnit, tableUnit, tableSize, val):

    pos = convertToMeter(fromUnit, val)
    size = convertToMeter(tableUnit, tableSize)

    return pos / size

class DXF:

    def __init__(self, dxfPath, cncWidth, cncHeight, units):

        self.TABLE_WIDTH = cncWidth
        self.TABLE_HEIGHT = cncHeight
        self.TABLE_UNIT = units

        self.DOC = ezdxf.readfile(dxfPath)
        self.MSP = self.DOC.modelspace()

        self.ENTITIES = []
        for e in self.MSP:
            self.ENTITIES.append(e)

        self.SELECTION = 0
        self.ENTITY_COUNT = len(self.ENTITIES)

        self.LENGTH_UNIT = self.DOC.header['$INSUNITS']

    def getNextEntity(self):

        if  self.SELECTION > (len(self.ENTITIES) - 1):
            self.SELECTION = 0

        return self.ENTITIES[0]

