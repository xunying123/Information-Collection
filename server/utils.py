from flask import Response
import json

def jsonify(obj):
    return Response(
        json.dumps(obj, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )
