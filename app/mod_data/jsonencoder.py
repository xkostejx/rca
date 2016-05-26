import json
import decimal
import datetime

class DbEncoder(json.JSONEncoder):
        def default(self, obj):
                if isinstance(obj, decimal.Decimal):
                        return str(obj)
                elif isinstance(obj, datetime.datetime):
                        return obj.strftime("%Y-%m-%d %H:%M:%S")
        	return json.JSONEncoder.default(self, obj)
