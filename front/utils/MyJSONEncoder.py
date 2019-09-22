import json
import datetime
import decimal  
import sqlalchemy
import time

class MyJSONEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, sqlalchemy.engine.result.ResultProxy):
            result = obj.fetchall()
            if len(result) == 1:
                return result[0]
            return result

        if isinstance(obj, sqlalchemy.engine.result.RowProxy):
            fields = {}
            for item in obj.items():
                fields[item[0]] = item[1]

            return fields

        if isinstance(obj.__class__, sqlalchemy.ext.declarative.DeclarativeMeta):
            return {c.name: getattr(obj, c.name, None) for c in obj.__table__.columns}

        if isinstance(obj, (datetime.datetime,)):  
            strTime = obj.strftime("%Y-%m-%d %H:%M:%S") 
            return strTime
            #return obj.isoformat()

        if isinstance(obj, (decimal.Decimal,)):  
            return str(obj)

        return json.JSONEncoder.default(self, obj)
