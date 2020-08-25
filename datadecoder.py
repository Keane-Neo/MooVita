#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from io import StringIO
import pandas as pd
import tkinter as tk

var = StringIO()

class data:

	# Session logging

	def session_log(_ti,report):
		print("Generating session log")
		
    # Find average voltage value from first and last 50 values
		def avg(num):
			return (sum(num) / len(num))
		ti = pd.read_csv(_ti, skiprows = 1) ## The labels on the first row is not neccesary
		var.write("##### Session Log ##### \n\n Start time: {} \n\n End time: {} \n\n Start voltage = {} \n\n End voltage = {}\n\n".format(ti.iloc[0][0], ti.iloc[len(ti.index)-1][0], avg(ti.iloc[1:50,29])/10, avg(ti.iloc[len(ti.index)-50 : len(ti.index)-1,29])/10 ) )
		
		


	# Trip logging

	def trip_log(_ti, _vs, report):
		print("Generating trip log")
		ti = pd.read_csv(_ti, skiprows = 1) ## The labels on the first row is not neccesary
		vs = pd.read_csv(_vs, skiprows = 1)
		i = 1
		if ti.iloc[0][8] == "Override" :
			var.write("##### Trip Log ##### \n\n Trip {}) Initial State: Manual at {} \n\n".format(i,ti.iloc[0][0]))
	
		elif ti.iloc[0][8] == "Drive" :
			var.write("##### Trip Log ##### \n\n Trip {}) Initial State: Auto at {} \n\n".format(i,ti.iloc[0][0]))
		else :
			var.write("##### Trip Log ##### \n\n Trip {}) Initial State: {} at {} \n\n".format(i,ti.iloc[0][8], ti.iloc[0][0]))
		i += 1
		 
		estop = 0
   
		# Skip the first iteration, initial state already printed
		iterrows = ti.iterrows()
		next(iterrows)  
		for index,row in iterrows:
			if ti.iloc[index][8] != ti.iloc[index-1][8] and ti.iloc[index][8] == "Override" :
				var.write(" Trip {}) Change in state: Manual at {} \n\n".format(i,ti.iloc[index][0]))
				i += 1
			elif ti.iloc[index][8] != ti.iloc[index-1][8] and ti.iloc[index][8] == "Drive" :
				var.write(" Trip {}) Change in state: Auto at {} \n\n".format(i,ti.iloc[index][0]))			
				i += 1
			elif ti.iloc[index][8] != ti.iloc[index-1][8] :			
				var.write(" Trip {}) Change in state: {} at {} \n\n".format(i,ti.iloc[index][8],ti.iloc[index][0]))
				i += 1

	    # check for e-stop, print localization score and timestamp
			if ti.iloc[index][8] == 'Estop' and ti.iloc[index][8] != ti.iloc[index-1][8]:
				estop = 1
				var.write(" Estop occured at {}\n\n".format(ti.iloc[index][0])) 
				for index,row in vs.iterrows():
					if vs.iloc[index][0]== ti.iloc[index][0] :
						var.write(" Localization_score = {}\n\n".format(vs.iloc[index][25]))
						break
				
				
		var.write(" End state: {} at {} \n\n".format(ti.iloc[index][8],ti.iloc[index][0]))
		
		

		if estop == 0 :
			var.write(" E-stop event did not occur \n\n") 

		     

	# check for software failure and print timestamp

	def check_software(_hb, report):
		print("Generating software log")
		hb = pd.read_csv(_hb, skiprows = 1)		
		var.write("##### Software Check #####\n\n")
		count = 0
		
		for index,row in hb.iterrows():
			if hb.iloc[index][10] < 0 and hb.iloc[index][10] != hb.iloc[index-1][10] :
				count += 1
				var.write(" {})'pclobjregonitor' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))

			if hb.iloc[index][15] < 0 and hb.iloc[index][15] != hb.iloc[index-1][15]:
				count += 1
				var.write(" {})'decisionmaker' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))
		        
			if hb.iloc[index][20] < 0 and hb.iloc[index][20] != hb.iloc[index-1][20]:
				count += 1
				var.write(" {})'missionplanner' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))
		        
		        
			if hb.iloc[index][25] < 0 and hb.iloc[index][25] != hb.iloc[index-1][25]:
				count += 1
				var.write(" {})'localization' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))
		        
		        
			if hb.iloc[index][30] < 0 and hb.iloc[index][30] != hb.iloc[index-1][30]:
				count += 1
				var.write(" {})'left_lidar' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))

		        
		        
			if hb.iloc[index][35] < 0 and hb.iloc[index][35] != hb.iloc[index-1][35] :
				count += 1
				var.write(" {})'right_lidar' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))

		        
		       
			if hb.iloc[index][40] < 0 and hb.iloc[index][40] != hb.iloc[index-1][40] :
				count += 1
				var.write(" {})'fused_lidar' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))

		        
		        
			if hb.iloc[index][45] < 0 and hb.iloc[index][45] != hb.iloc[index-1][45] :
				count += 1
				var.write(" {})'phidgetencoder' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))
		        
		        
			if hb.iloc[index][50] < 0 and hb.iloc[index][50] != hb.iloc[index-1][50] :
				count += 1
				var.write(" {})'imu' module failure occured at {} \n\n".format(conut,hb.iloc[index][0]))

		        
		        
			if hb.iloc[index][55] < 0 and hb.iloc[index][55] != hb.iloc[index-1][55] :
				count += 1
				var.write(" {})'texasinstrument' module failure occured at {} \n\n".format(count,hb.iloc[index][0]))
		               

		if count == 0 :
			var.write(" There was no module failure")
		tk.Label(report, text = var.getvalue()).pack()

	def save():
		fileName=filedialog.asksaveasfilename(title = "Save as", filetypes=[("Txt files", "*.txt")])
		f = open(fileName, "w+")
		for x in var.getvalue():
			f.write(x)
		f.close()	
		
		
	

