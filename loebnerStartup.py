import json,re,threading #,aiml
from socketIO_client import SocketIO, BaseNamespace
#from NLP import NLP
from nltk.stem.snowball import SnowballStemmer
from time import sleep

stemmer = SnowballStemmer('english')

# AIML memory
#print "Starting to learn (~13 sec)"
#k = aiml.Kernel()
#k.saveFilepath('/root/Scripts/Alicia/memory/aiml/')
#k.learn("*")

url = '127.0.0.1'
port = '8080'
id = 'ai0'
to = 'judge0'
secret = 'abc123'

register = [{'status': 'register'}]
roundInfo = [{'status': 'roundInformation'}]

lastMessage,status = '',''
roundNum = 0

def shape(word):
    word_shape = 'other'
    if re.match('[0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+$', word):
        word_shape = 'number'
    elif re.match('\W+$', word):
        word_shape = 'punct'
    elif re.match('[A-Z][a-z]+$', word):
        word_shape = 'capitalized'
    elif re.match('[A-Z]+$', word):
        word_shape = 'uppercase'
    elif re.match('[a-z]+$', word):
        word_shape = 'lowercase'
    elif re.match('[A-Z][a-z]+[A-Z][a-z]+[A-Za-z]*$', word):
        word_shape = 'camelcase'
    elif re.match('[A-Za-z]+$', word):
        word_shape = 'mixedcase'
    elif re.match('__.+__$', word):
        word_shape = 'wildcard'
    elif re.match('[A-Za-z0-9]+\.$', word):
        word_shape = 'ending-dot'
    elif re.match('[A-Za-z0-9]+\.[A-Za-z0-9\.]+\.$', word):
        word_shape = 'abbreviation'
    elif re.match('[A-Za-z0-9]+\-[A-Za-z0-9\-]+.*$', word):
        word_shape = 'contains-hyphen'
    return word_shape

def message(*args):
	global roundNum
	global status
	global lastMessage
	if not '\\' in str(args): return
	mess = str(args).replace('\\','')
	if 'content' in mess: 
		mess = mess.split('content')[1].split(':"')[1].split('"')[0]
		if mess != lastMessage:
			print "Message from judge: "+mess
			try: text = k.respond(mess,'human')
			except:
				print "Message Error"
				text = ''
				pass
			if text: socketIO.emit('message', toJSON([{'to':to,'content':text}]))
			lastMessage = mess
	elif 'newRound' in mess: print "New Round initiated"
	elif 'startRound' in mess: print "Round started"
	elif 'endRound' in mess: print "Round has ended"
	elif 'roundInformation' in mess: 
		if roundNum == '-1': print "Connected to node server"
		else:
			roundNum = mess.split('roundNumber')[1].split(':')[1].split(',')[0]
			status = mess.split('status')[1].split(':"')[1].split('"')[0]
			print "Current round number is "+roundNum+". The status is "+status

def toJSON(map):
	map[0]['id'] = id
	map[0]['secret'] = secret
	return json.dumps(map[0],separators=(',',':'))

while True:
	print "Trying to connect to node server"
	try:
		socketIO = SocketIO(url,port)
		socketIO.emit('control', toJSON(register))
		socketIO.on('message', message)
		socketIO.emit('control', toJSON(roundInfo))
		socketIO.wait()
	except:
		print "Disconnected from the pipe"
	sleep(5)





