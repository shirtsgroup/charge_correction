

def top_reader(top):
    # read top file and create dictionary of lj parameters and charge
    radius = {}
    names = {}
    charge = []
    ratio = 5.6123
    next = 0
    next_charge = 0
    with open(top) as infile:
        for line in infile:
            if 'atomtypes' in line:
                next = 1
            elif '[ atoms ]' in line:
                next_charge = 1
            elif next is 1:
                line_temp = line.split()
                if len(line_temp) > 1:
                    if next is 1 and line_temp[0][0] is not ';':
                        radius[line_temp[0]] = ratio * float(line_temp[6])
                else:
                    next = 0
            elif next_charge is 1:
                line_temp = line.split()
                if len(line_temp) > 1:
                    if line_temp[0][0] is not ';' and line_temp[3] not in 'WAT':
                        charge.append(line_temp[6])
                        names[line_temp[4]] = line_temp[1]
                else:
                    next_charge = 0

    return radius, charge, names


def make_pqr(gro, radius, charge, name, types):

    f = open(gro, 'r')
    lines = f.readlines()
    f.close()

    out = gro.replace('.gro', '_' + types + '.pqr')
    outfile = open(out, 'w')
    l_num = 0

    for l in lines:
        line_temp = l.split()
        if len(line_temp) > 4 and 'WAT' not in line_temp[0]:
            a_number = line_temp[2]
            a_name = line_temp[1]
            a_type = name[line_temp[1]]
            print(a_type)
            a_radius = radius[a_type]
            a_charge = charge[l_num]
            a_res = line_temp[0]
            a_res_num = a_res[0]
            a_x = float(line_temp[3]) * 10
            a_y = float(line_temp[4]) * 10
            a_z = float(line_temp[5]) * 10
            if a_type in ['Na+', 'Cl-', 'Na']:
                l_num = l_num
            else:
                l_num += 1
            if a_res in types:
                a_charge = a_charge
            else:
                a_charge = 0
            n_line = 'ATOM' + ' ' + a_number + ' ' + a_name + ' ' + a_res + ' ' + a_res_num + ' ' + str(a_x) + ' ' + \
                     str(a_y) + ' ' + str(a_z) + ' ' + str(a_charge) + ' ' + str(a_radius) + '\n'

            outfile.write(n_line)
    outfile.write('TER \n')
    outfile.write('END \n')


# reads a gro file and a top file and creates a pqr file
# water is removed during the process
f_name = 'solvent'


top_file = f_name + '.top'
gro_file =  f_name + '.gro'
# types = ['1HST', '2GST']
types = ['1GST', ' ']

radius_dic, charge, names = top_reader(top_file)
for n in types:
    make_pqr(gro_file, radius_dic, charge, names, n)
