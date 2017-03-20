#!/home/pengfeil/AMBER/amber16/amber16/miniconda/bin/python
# Filename: change_crd.py
from __future__ import print_function
import parmed as pmd
from numpy import array
from optparse import OptionParser

parser = OptionParser("Usage:  -i input_file -p top_file -c crd_file -o out_crd_file --prog program")
parser.add_option("-i", dest="inputf", type='string',
                  help="Input file name")
parser.add_option("-p", dest="topf", type='string',
                  help="Topology file name")
parser.add_option("-c", dest="crdf", type='string',
                  help="Coordinate file name")
parser.add_option("-o", dest="outputf", type='string',
                  help="Output coordinate file name")
parser.add_option("--prog", dest="program", type='string',
                  help="Program: amber/charmm")
(options, args) = parser.parse_args()

# Read the input file, which should have lines with information as:
# AtomNum Crdx Crdy Crdz
# For the atoms whose coordinates need to be changed
val_list = []

inputf = open(options.inputf, 'r')
ln = 1
for line in inputf:
    line = line.split()
    if '\n' in line:
        line.remove('\n')
    if ',' in line:
        line.remove(',')
    if '' in line:
        line.remove('')
    if ' ' in line:
        line.remove(' ')
    if ':' in line:
        line.remove(':')
    # Blank line
    if (len(line) == 0):
        continue
    # Comment
    elif (line[0][0] == '#'):
        continue
    elif (len(line) == 4):
        line = (int(line[0]), float(line[1]), float(line[2]), float(line[3]))
        val_list.append(line)
    elif (len(line) != 4):
        raise ValueError('There are not four numbers in the line number %d' %ln)
    ln = ln + 1

if options.program == 'amber':
    # Load the molecule
    mol = pmd.load_file(options.topf, options.crdf)
    mol_crd = pmd.amber.Rst7(options.crdf)
elif options.program == 'charmm':
    # Load the molecule
    mol_crd = pmd.charmm.CharmmCrdFile(options.crdf)

for i in mol_crd.coordinates:
    pure_mol_crd = i

for i in xrange(len(val_list)):
    val = val_list[i]
    atnum, crdx, crdy, crdz = val
    print("%s %s" %('Atom Name is :', mol.atoms[atnum-1].name))
    print("Old coordinates are :")
    print("%12.6f %12.6f %12.6f" %(pure_mol_crd[atnum-1][0], pure_mol_crd[atnum-1][1], pure_mol_crd[atnum-1][2]))
    pure_mol_crd[atnum-1][0] = crdx
    pure_mol_crd[atnum-1][1] = crdy
    pure_mol_crd[atnum-1][2] = crdz
    print("New coordinates are :")
    print("%12.6f %12.6f %12.6f" %(pure_mol_crd[atnum-1][0], pure_mol_crd[atnum-1][1], pure_mol_crd[atnum-1][2]))

# Print out the final crd file
if options.program == 'charmm':
    #inter_mol.save(options.output, format='charmmcrd', overwrite=True)
    atomno = mol_crd.atomno
    resno = mol_crd.resno
    resname = mol_crd.resname
    atname = mol_crd.atname
    segid = mol_crd.segid
    resid = mol_crd.resid
    weighting = mol_crd.weighting
    w_output = open(options.outputf, 'w')
    w_outpdb = open(options.outputf+'.pdb', 'w')
    print('* GENERATED BY PARMED (HTTPS://GITHUB.COM/PARMED/PARMED)\n', end='', file=w_output)
    print('*\n', end='', file=w_output)
    print('%10d  EXT\n' % len(atomno), end='', file=w_output)
    for i in xrange(len(atomno)):
        print('%10d%10d  %-8s  %-8s%20.10f%20.10f%20.10f  %-8s  '
               '%-8s%20.10f\n' % (atomno[i], resno[i], resname[i], atname[i], 
               inter_crd[i][0], inter_crd[i][1], inter_crd[i][2], segid[i],
               resid[i], weighting[i]), end='', file=w_output)
        if atname[i] == 3:
	    print("%-6s%5d %4s %-4s%1s%4d   %8.3f%8.3f%8.3f%6.2f%6.2f" %('ATOM', atomno[i], \
	          atname[i], resname[i], ' ', resid[i], inter_crd[i][0], inter_crd[i][1], \
                  inter_crd[i][2], 1.00, 0.00), file=w_outpdb)
        else:
            print("%-6s%5d %4s %-4s%1s%4d   %8.3f%8.3f%8.3f%6.2f%6.2f" %('ATOM', atomno[i], \
                  atname[i].center(4), resname[i], ' ', resid[i], inter_crd[i][0], inter_crd[i][1], \
                  inter_crd[i][2], 1.00, 0.00), file=w_outpdb)
    w_output.close()
    w_outpdb.close()
elif options.program == 'amber':
    mol.positions = pure_mol_crd
    mol.coordinates = pure_mol_crd
    mol.save(options.outputf, format='rst7', overwrite=True)
    mol.save(options.outputf+'.pdb', format='pdb', overwrite=True)

