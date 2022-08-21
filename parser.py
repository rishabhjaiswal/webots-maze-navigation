import itertools
import logging
import os

# For the next line, use logging.WARN to turn off debug print, use
# logging.DEBUG to turn on
logging.basicConfig(level=os.getenv('LOGLEVEL', logging.WARN))
logger = logging.getLogger(__name__)


def skip_pass(marker, lines):
    """
    Skip until reach the line which contains the marker, then also skip
    the marker line
    """
    result = itertools.dropwhile(
        lambda line: marker not in line,  # Condition
        lines)                            # The lines
    next(result)                          # skip pass the markers
    return result

def take(marker, lines):
    """
    Take and return those lines which contains a marker
    """
    result = itertools.takewhile(
        lambda line: marker not in line,      # Condition
        lines)                            # The lines
    
    return result

def parse_walls(lines):
    """
    Parse one block of 'Walls'
    """
    point_lines = take('}', lines)
    a={}
    for i in point_lines:
        if 'translation' in i:
            a['translation']=parse_translate(i)
        if 'rotation' in i:
            a['rotation']=parse_translate(i)
        if 'size' in i:
            a['size']=parse_translate(i)
    return a

def parse_translate(line):
    """
    Given a line such as: "translate 5 6 7", return [5.0, 6.0, 7.0]
    """
    translate = [float(x) for x in line.split()[1:]]
    return translate

def extractDataFromVRML(root):
    walls = []
    with open(root + '.wbt') as infile:
        for line in infile:
            if 'Wall' in line:
                a_set = parse_walls(lines=infile)
                walls.append(a_set)
    return walls


# main
walls = extractDataFromVRML('empty')
for i in walls:
    print(i)