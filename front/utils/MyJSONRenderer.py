from flask_api.renderers import BaseRenderer
from front.utils.MyJSONEncoder import MyJSONEncoder
import json

class MyJSONRenderer(BaseRenderer):
    media_type = 'application/json'
    charset = None

    def render(self, data, media_type, **options):
        # Requested indentation may be set in the Accept header.
        try:
            indent = max(min(int(media_type.params['indent']), 8), 0)
        except (KeyError, ValueError, TypeError):
            indent = None
        # Indent may be set explicitly, eg when rendered by the browsable API.
        indent = options.get('indent', indent)
        return json.dumps(data, cls=MyJSONEncoder, ensure_ascii=False, indent=indent)
