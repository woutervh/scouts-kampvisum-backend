import logging
from django.db import models


logger = logging.getLogger(__name__)


class OptionalDateField(models.DateField):

    def __init__(self, *args, **kwargs):
        logger.info('ARGS: %s', args)
        # args['auto_now'] = False
        # args['auto_now_add'] = False
        # args['blank'] = True
        # args['null'] = True
        super(OptionalDateField, self).__init__(*args, **kwargs)



