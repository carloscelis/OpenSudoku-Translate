# text2opensudoku.py
# Export a Sudoku text file in OpenSudoku format
# Author Carlos Celis Flen-Bers

import sys, getopt
from os.path import basename
import lxml.etree as ET
from datetime import date
from string import maketrans

def usage(script):
  print 'Usage: ', script, ' OPTIONS'
  print '  OPTIONS: '
  print '    -h, --help : This help. '
  print '    -i FILE, --input=FILE : Text file input'
  print '    -o FILE, --output=FILE : XML Opensudoku file output'
  print '    -l LEVEL, --l=LEVEL : Set Level string from Sudokus into input file'

def main():
    in_file = None
    found_if = False
    out_file = 'output.opensudoku'
    levelstr = 'Undefinied'
    verbose = False
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "i:ohlv", ["help", "input=","output=", "level=", "verbose"])
    except getopt.GetoptError:          
        usage(sys.argv[0])
        sys.exit(2)                     
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
            sys.exit()                  
        elif opt in ("-i", "--input"):
            in_file = arg
            found_if = True
        elif opt in ("-o", "--output"):
            out_file = arg
        elif opt in ("-l", "--level"):
            levelstr = arg
        elif opt in ("-v", "--verbose"):
            verbose = True

    # file Input is required
    if not found_if:
      print "-i is required"
      usage(sys.argv[0])
      sys.exit(2)
      
    if verbose:
      print 'OPTIONS: ', opts
      print 'INPUT: ', in_file
      print 'OUTPUT: ', out_file
      print 'LEVEL: ', levelstr

    f = open(in_file)
    lines = f.readlines()
    root = ET.Element("opensudoku")
    print '  Sudokus: ', + len(lines)

    #Generating tag
    name =  ET.SubElement(root, "name")
    name.text = basename(in_file)

    author =  ET.SubElement(root, "author")
    author.text = 'celis flen-bers'

    description =  ET.SubElement(root, "description")
    description.text = 'File generated from text file \'' + basename(in_file) + '\''

    comment =  ET.SubElement(root, "comment")
    comment.text = 'Sudokus: ' + str(len(lines))

    created =  ET.SubElement(root, "created")
    created.text = str(date.today())

    source =  ET.SubElement(root, "source")
    source.text = 'celis flen-bers'

    level =  ET.SubElement(root, "level")
    level.text = levelstr

    sourceURL =  ET.SubElement(root, "sourceURL")
    sourceURL.text = 'http://celisflenbers.wordpress.com'

    intab = '.='
    outtab = '00'
    trantab = maketrans(intab, outtab)
    
    # Games
    for l in lines:

      l = l.translate(trantab)
      gameet = ET.SubElement(root, "game")
      gameet.attrib['data'] = l[0:80]

    tree = ET.ElementTree(root)
    tree.write(out_file, pretty_print=True)

if __name__ == "__main__":
   main()
