#!/usr/bin/env python3
##############################################################################
# Description:                                                               #
# If don´t exists, create a CSV file with the SATART and END datetime period #
# wich other scripts can use as parameter                                    #
# Written by Diego Viane Github: https://github.com/diegoviane2              #
##############################################################################

#####################
# DATETIME FORMAT:  #
# dd/mm/aaaa HH:MM  #
#####################

import csv
import argparse


# Handling arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--start", required=True, help="Start Period")
ap.add_argument("-e", "--end", required=True, help="End Period")
args = vars(ap.parse_args())


def validator(data):
    

def append_date(start_period, end_period):
    # Adiciona nova linha com as informações recebidas via argumentos em formato CSV
    with open('launch_period.csv', 'a+', newline='')as file:
        writer = csv.writer(file)
        writer.writerow([start_period, end_period])


#Call Function
print ("  [ Initializing task - Write file ]")
print ("  [ Writing ... Start-Period: " + str(args['start']) + " End-Period: " + str(args['end']) + " ... ]")
append_date(str(args['start']),str(args['end']))
print ("  [ Write file ... ] [DONE]")