#!/usr/bin/python

import os
import glob
import time
import datetime
import json

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder1 = glob.glob(base_dir + '28*7c8')[0]
device_folder2 = glob.glob(base_dir + '28*cce')[0]
device_file1 = device_folder1 + '/w1_slave'
device_file2 = device_folder2 + '/w1_slave'

data = {}
ts = time.time()
dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
data['timestamp'] = dt

def read_temp_raw1():
	f1 = open(device_file1, 'r')
	lines1 = f1.readlines()
	f1.close()
	return lines1

def read_temp1():
	temp1Cal = -3.2
	lines = read_temp_raw1()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw1()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		temp_f = temp_f + temp1Cal
		return temp_f

def read_temp_raw2():
	f2 = open(device_file2, 'r')
	lines2 = f2.readlines()
	f2.close()
	return lines2

def read_temp2():
	temp2Cal = .87
	lines = read_temp_raw2()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw2()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		temp_f = temp_f + temp2Cal
		return temp_f

data['temp1']= str(read_temp1())
data['temp2']= str(read_temp2())

json_data = json.dumps(data, sort_keys=True)

print(json_data)
time.sleep(1)
