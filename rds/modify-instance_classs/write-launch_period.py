#!/usr/bin/env python3
##############################################################################
# Description:                                                               #
# If don´t exists, create a CSV file with the SATART and END datetime period #
# wich other scripts can use as parameter                                    #
# Written by Diego Viane Github: https://github.com/diegoviane2              #
##############################################################################
#                   #
#####################
# DATETIME FORMAT:  #
# dd/mm/aaaa HH:MM  #
#####################

import re
import csv
import argparse



# Handling arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--start", required=True, help="Start Period")
ap.add_argument("-e", "--end", required=True, help="End Period")
args = vars(ap.parse_args())

start = args['start']
end = args['end']

def valid(data):
    pattern = re.compile(r'\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}')
    valid = re.match(pattern, data)
    if valid:
        return True
    else:
        return False

def append_date(start_period, end_period):
    # Adiciona nova linha com as informações recebidas via argumentos em formato CSV
    with open('launch_period.csv', 'a+', newline='')as file:
        writer = csv.writer(file)
        writer.writerow([start_period, end_period])


#Call Function
print ("[ Initializing task - Schedule Launch Period ]")
if valid(start) and valid(end):    
    print ("[ Writing ... Start-Period: " + str(args['start']) + " End-Period: " + str(args['end']) + " ... ]")
    append_date(str(start),str(end))
    print ("[ Write to file ... ] [ OK ]")
    print('[ Finalizing task ... ] [ DONE ]')
    print("[ TASK: Schedule Launch Period  ... ] [ DONE ]")
else:
    print("[ Error: One of the values is invalid ... ] [ WARNING ]")
    print("[ Accepted formats: dd/mm/aaaa HH:MM  ... ] [ WARNING ]")
    print("[ TASK: Schedule Launch Period  ... ] [ FAILED ]")