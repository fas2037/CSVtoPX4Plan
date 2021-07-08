# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Ctrl+F8 to toggle the breakpoint.

import csv
import sys
from shutil import copyfile


def parse_csv(csvFile, planFile):
    copyfile('scratch.plan', planFile)
    output = open(planFile, "a")

    with open(csvFile) as csvfile:
        mission_input = csv.reader(csvfile)
        mission_items = ''
        for row in mission_input:
            mission_items += create_mission_item(row)
        mission_items = mission_items[:-1]
        mission_items += "\n\t\t],\n"
        output.write(mission_items)

    output.write(planned_home())
    output.write(ending())


def create_speed_item(speed):
    result = '\n{\n'
    same = ('\t\"autoContinue\": true,\n'
            '\"command\": 178,\n'
            '\"doJumpId\": 3,\n'
            '\"frame\": 2,\n'
            '\"params\": [\n'
            '\t1,\n'
            )
    result += '\t'.join(same.splitlines(True))
    result += "\t\t"
    result += speed
    result += ",\n"
    same2 = ('\t\t-1,\n'
             '\t0,\n'
             '\t0,\n'
             '\t0,\n'
             '\t0\n'
             '],\n'
             '\"type\": \"SimpleItem\"\n'
             )
    result += '\t'.join(same2.splitlines(True))
    result += '},'
    return result


def create_mission_item(row):
    result = create_speed_item(row[3])
    result += '\n{\n'
    result += '\t\"AMSLAltAboveTerrain\": null,\n'
    result += '\t"Altitude": '
    result += row[2]
    result += ',\n'
    same = ('\t\"AltitudeMode\": 1,\n'
            '\"autoContinue\": true,\n'
            '\"command\": 16,\n'
            '\"doJumpId\": 1,\n'
            '\"frame\": 3,\n'
            '\"params\": [\n'
            '\t0,\n'
            '\t0,\n'
            '\t0,\n'
            '\tnull,\n'
            )
    result += '\t'.join(same.splitlines(True))
    result += '\t\t' + row[0]
    result += ',\n'
    result += '\t\t' + row[1]
    result += ',\n'
    result += '\t\t' + row[2]
    result += '\n'
    result += '\t],\n'
    result += '\t\"type\": \"SimpleItem\"\n'
    result += '},'

    return '\t\t\t'.join(result.splitlines(True))


def ending():
    result = ('\t\t\"vehicleType": 2,\n'
              '\t\t\"version": 2\n'
              '\t},\n'
              '\t\"rallyPoints": {\n'
              '\t\t\"points": [\n'
              '\t\t],\n'
              '\t\t\"version": 2\n'
              '\t},\n'
              '\t\"version": 1\n'
              '}\n'
              )
    return result


def planned_home():
    result = ('\"plannedHomePosition": [\n'
              '48.6869697,\n'
              '11.5324518,\n'
              '365.2486635615994\n'
              '],\n'
              )
    return result


def print_usage():
    print("Usage: converter.py inputFile.csv outputFile.plan")
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Not enough or too many arguments!")
        print_usage()

    inFile = sys.argv[1]
    outFile = sys.argv[2]

    if not ('.' in inFile and inFile.split('.')[1] == 'csv'):
        print("Wrong file format")
        print_usage()

    if not ('.' in outFile and outFile.split('.')[1] == 'plan'):
        print("Wrong file format")
        print_usage()

    if outFile == "scratch.plan":
        print("Don't use scratch.plan as output!")
        print_usage()
    print("converting...")
    parse_csv(inFile, outFile)
    print("done")
