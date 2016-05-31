import json
import decimal
import datetime

class DbEncoder(json.JSONEncoder):
        def default(self, obj):
                if isinstance(obj, decimal.Decimal):
                        return str(obj)
                elif isinstance(obj, datetime.datetime):
                        return obj.strftime("%d.%m.%Y %H:%M:%S")
        	return json.JSONEncoder.default(self, obj)

class data2json():
	@staticmethod
	def fromDB(data, custom = False):
		if custom:
			return json.dumps({"data" : [d.to_dict() for d in data]})
		else:
			return json.dumps({"data" : [dict(d) for d in data]}, cls = DbEncoder)
