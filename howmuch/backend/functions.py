# -*- coding: utf8 -*- 
import datetime

def get_timestamp(date):
	delta = datetime.datetime.now() - date
	deltaSeconds = delta.total_seconds()

	if deltaSeconds < 60:
		return "%s segundos" % (int(deltaSeconds))
	elif deltaSeconds >= 60 and deltaSeconds < 3600:
		return "%s minutos" % (int(deltaSeconds/60))
	elif deltaSeconds >= 3600 and deltaSeconds < 86400:
		return "%s horas" % (int(deltaSeconds/3600))
	elif deltaSeconds >= 86400 and deltaSeconds < 31536000:
		return "%s dias" % (int(deltaSeconds/86400))
	else:
		return "%s años" % (int(deltaSeconds/31536000)) 
