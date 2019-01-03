import csv
import sys
import re
import math

## process logic analyzer sample output into pulse times

# constants
CSV_COLUMN_TIME = 0
CSV_COLUMN_VALUE = 1


def processCsvInput(csvData):
    outputData = csvData
    # strip first row if it is a column header
    if re.match('\W+', csvData[0][CSV_COLUMN_TIME]) is not None or re.match('\W+', csvData[0][CSV_COLUMN_VALUE]) is not None :
        print 'first line is column header'
        outputData.pop(0)

    # strip first row if the value is low
    if csvData[0][CSV_COLUMN_VALUE] == 0:
        print 'first sample is low'
        outputData.pop(0)



def processSampleRow(row):
    # skip text rows
    if re.match('^Time', row[CSV_COLUMN_TIME]) is not None or re.match('^\s*Channel', row[CSV_COLUMN_VALUE]) is not None:
        return False

    # convert start time to a float
    try:
        startTime = float(row[CSV_COLUMN_TIME])
        return {
            'startTime': int(math.ceil(startTime*(10**6))),
            'value': int(row[CSV_COLUMN_VALUE])
        }
    except:
        return False


def __main__(args):
    # check for arguments
    if len(args) <= 1:
        print 'ERROR: Expecting argument to identify CSV sample file'
        sys.exit(2)
    # assign csv file
    csvFile = args[1]

    # initialize variables to be used for reading the samples
    pulseData = []

    # read csv file
    with open(csvFile, 'r') as f:
        print '> Converting samples from file %s'%(csvFile)
        reader = csv.reader(f)
        prevRowData = False
        print ' ... '

        ## process samples into pulse-widths with values and durations
        for row in reader:
             #print row
             rowData = processSampleRow(row)
             #print lineData
             if prevRowData is not False:
                # find the duration of the pulse described on the previous row
                pulse = {
                    'value': prevRowData['value'],
                    'duration': rowData['startTime'] - prevRowData['startTime']
                }
                # add it to the list of pulses
                pulseData.append(pulse)
                #print pulse

             prevRowData = rowData
        f.close()


        ## output pulses into format required by fast-gpio
        print ' ... '
        # create the name of the pulse file
        pulseFile = re.sub(r'\.csv', '.pulse', csvFile, flags=re.IGNORECASE)
        # get rid of the first pulse-width if it's low
        if pulseData[0]['value'] == 0:
            pulseData.pop(0)

        # add an additional pulse-width if the last one is high
        if pulseData[-1]['value'] == 1:
            pulseData.append({
                'value': 0,
                'duration': 5000
            })

        # open the pulse file for writing
        with open(pulseFile, 'w') as fOut:
            # write out each of the pulses
            for point in pulseData:
                # write the pulse duration
                fOut.write(str(point['duration']))
                if point['value'] == 1:
                    fOut.write(', ')
                else:
                    fOut.write(', ')

            # add a closing 0,0
            fOut.write('0,0\n')

            # close the file
            fOut.close()
            print '> Pulse file written: %s'%(pulseFile)




if __name__ == '__main__':
    __main__(sys.argv)
