from typing import List

from django.db import transaction, connections
from django.core.management.base import BaseCommand

from apps.visums.models import CampVisum
from apps.visums.settings import VisumSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes issue 93032 https://redmine.inuits.eu/issues/93032"
    exception = True

    @transaction.atomic
    def handle(self, *args, **kwargs):
        name_date_check = VisumSettings.get_camp_date_check_name()
        visums = []
        with connections['default'].cursor() as cursor:
            cursor.execute("select vc.id as id from visums_campvisum vc")

            visums = cursor.fetchall()

            for visum in visums:
                cursor.execute(
                    f"select dc.start_date as start_date, dc.end_date as end_date from visums_linkeddurationcheck dc left join visums_linkedcheck lc on dc.linkedcheck_ptr_id = lc.id left join visums_linkedsubcategory sc on sc.id = lc.sub_category_id left join visums_linkedcategory cat on cat.id = sc.category_id left join visums_linkedcategoryset cs on cs.id = cat.category_set_id left join visums_check c on c.id = lc.parent_id where	dc.start_date is not null and dc.end_date is not null and c.name = '{name_date_check}' and cs.visum_id = '{visum[0]}'"
                )
                result = cursor.fetchone()

                if result:
                    cursor.execute(
                        f"update visums_campvisum set start_date='{result[0]}', end_date='{result[1]}' where id='{visum[0]}'"
                    )
            
        return None
