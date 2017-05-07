#! /usr/bin/python
import RPi.GPIO as GPIO
import time
import MySQLdb

Ledslot1free = 36
Ledslot1reserve = 38
Ledslot1close = 40

Ledslot2free = 35
Ledslot2reserve = 37
Ledslot2close = 32

Ledslot3free = 29
Ledslot3reserve = 31
Ledslot3close = 33



hostname = 'next-tech.techlimittv.eu'
username = 'NextTech'
password = '1215123@GJK'
database = 'projectparking'

def doQuery1( conn, id, state) :
        cur = conn.cursor()
        sql = "UPDATE slots SET status=\'"
        sql = sql +str(state)
        sql = sql + "\'"
	sql = sql + " WHERE id=\'"
	sql = sql +str(id)
	sql = sql + "\'"
	cur.execute(sql)


def doQuery2( conn,id) :
	cur = conn.cursor()
	cur.execute( "SELECT id, status FROM slots WHERE id="+str(id) )
    
	for id, status  in cur.fetchall() :
        	print id,status
	return status 


db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=database)

curs=db.cursor()

def checkdist1():
	GPIO.output(16, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(16, GPIO.LOW)
	while not GPIO.input(18):
		pass
	t1 = time.time()
	while GPIO.input(18):
		pass
	t2 = time.time()
	return 100*(t2-t1)*340/2
def checkdist2():
        GPIO.output(13, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(13, GPIO.LOW)
        while not GPIO.input(11):
                pass
        t1 = time.time()
        while GPIO.input(11):
                pass
        t2 = time.time()
        return 100*(t2-t1)*340/2

def changestate1(statement):
	if (statement=="free"):
        	GPIO.output(Ledslot1free, GPIO.LOW)
	        GPIO.output(Ledslot1reserve, GPIO.HIGH)
	        GPIO.output(Ledslot1close, GPIO.HIGH)

	elif (statement=="reserve"):
        	GPIO.output(Ledslot1free, GPIO.HIGH)
        	GPIO.output(Ledslot1reserve, GPIO.LOW)
        	GPIO.output(Ledslot1close, GPIO.HIGH)
	else:
        	GPIO.output(Ledslot1free, GPIO.HIGH)
        	GPIO.output(Ledslot1reserve, GPIO.HIGH)
        	GPIO.output(Ledslot1close, GPIO.LOW)		

def changestate2(statement):
        if (statement=="free"):
                GPIO.output(Ledslot2free, GPIO.LOW)
                GPIO.output(Ledslot2reserve, GPIO.HIGH)
                GPIO.output(Ledslot2close, GPIO.HIGH)
        elif (statement=="reserve"):
                GPIO.output(Ledslot2free, GPIO.HIGH)
                GPIO.output(Ledslot2reserve, GPIO.LOW)
                GPIO.output(Ledslot2close, GPIO.HIGH)
        else:
                GPIO.output(Ledslot2free, GPIO.HIGH)
                GPIO.output(Ledslot2reserve, GPIO.HIGH)
                GPIO.output(Ledslot2close, GPIO.LOW)

def changestate3(statement):
        if (statement=="free"):
                GPIO.output(Ledslot3free, GPIO.LOW)
                GPIO.output(Ledslot3reserve, GPIO.HIGH)
                GPIO.output(Ledslot3close, GPIO.HIGH)
        elif (statement=="reserve"):
                GPIO.output(Ledslot3free, GPIO.HIGH)
                GPIO.output(Ledslot3reserve, GPIO.LOW)
                GPIO.output(Ledslot3close, GPIO.HIGH)
        else:
                GPIO.output(Ledslot3free, GPIO.HIGH)
                GPIO.output(Ledslot3reserve, GPIO.HIGH)
                GPIO.output(Ledslot3close, GPIO.LOW)



GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(18,GPIO.IN)
GPIO.setup(13,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(11,GPIO.IN)


GPIO.setup(Ledslot1free, GPIO.OUT)
GPIO.setup(Ledslot1reserve, GPIO.OUT)
GPIO.setup(Ledslot1close, GPIO.OUT)

GPIO.setup(Ledslot2free, GPIO.OUT)
GPIO.setup(Ledslot2reserve, GPIO.OUT)
GPIO.setup(Ledslot2close, GPIO.OUT)

GPIO.setup(Ledslot3free, GPIO.OUT)
GPIO.setup(Ledslot3reserve, GPIO.OUT)
GPIO.setup(Ledslot3close, GPIO.OUT)

status1=doQuery2(db,2)
changestate1(status1)

status2=doQuery2(db,3)
changestate2(status2)

status3=doQuery2(db,4)
changestate3(status3)
time.sleep(5)


try:
	while True :
		if(status1 != "reserve"):
			distance1 = checkdist1()
			if (distance1 < 20.0):
				doQuery1(db,2,"close")
				db.commit()
				changestate1("close")
				print 'the parking Slot1 is close'
				print '%0.2f cm' %distance1
				
			else :
				doQuery1(db,2,"free")
				db.commit()
				changestate1("free")
				print 'The parking slot1  is free'
				print '%0.2f cm' %distance1
		time.sleep(1)

		if(status2 != "reserve"):
			distance2 = checkdist2()		
			if (distance2 < 20.0):
        	                doQuery1(db,3,"close")
                	        db.commit()
				changestate2("close")
				print 'the parking slot2 is close'
                        	print '%0.2f cm' %distance2
	
        	        else :
                	        doQuery1(db,3,"free")
                        	db.commit() 
				changestate2("free")
                        	print 'The parking slot2  is free'
                        	print '%0.2f cm' %distance2

		time.sleep(1)
		status1=doQuery2(db,2)
		status2=doQuery2(db,3)
		status3=doQuery2(db,4)						
except KeyboardInterrupt:
	GPIO.cleanup()
db.close()
