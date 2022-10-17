import datetime

from apps.camps.models import CampYear

from scouts_auth.groupadmin.scouts import ScoutsTemporalDetails


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampYearService:
    def create_year(self, request, **data):
        return self.get_or_create_year(request, data.get("year", None))

    def get_or_create_year(self, request, date=None):
        """
        Returns a CampYear instance.

        If a date is not supplied, datetime.date.today() is used.
        Date resolution will follow these rules:
        - A CampYear is searched with a start_date after the supplied date
            and an end_date before the supplied date. If not found:
        - A CampYear is created.
        - If the current month is July (the start of the camp season) or later,
            then the CampYear is considered to mean the next scout year.
        - If the month is earlier than July, the scout year starting in the
            previous calendar year is returned
        """
        current = datetime.date.today()
        if date is None:
            date = current
        # date is a year
        if not isinstance(date, datetime.date):
            date = datetime.date(date, current.month, current.day)

        camp_year = self._get_year(date=date)
        if camp_year is not None:
            return camp_year
        else:
            return self._create_year(date=date)

    def get_current_camp_year(self) -> CampYear:
        return self._get_year(date=datetime.datetime.today())

    def get_or_create_current_camp_year(self) -> CampYear:
        return self.get_or_create_year(None, date=datetime.datetime.today())

    def _get_year(self, date: datetime.date) -> CampYear:
        (
            start_date,
            end_date,
        ) = ScoutsTemporalDetails.get_start_and_end_date_of_camp_year(date)
        # logger.debug("Start date of camp year for date %s: %s", date, start_date)
        qs = CampYear.objects.filter(start_date__lte=start_date, end_date__gte=end_date)
        if qs.count() == 1:
            logger.debug("Found a year: %s", qs[0])
            return qs[0]

        return None

    def _create_year(self, date: datetime.date):
        instance = CampYear()

        start_date = ScoutsTemporalDetails.get_start_of_camp_year(date)
        end_date = ScoutsTemporalDetails.get_end_of_camp_year(date)

        # logger.debug(
        #     "Creating camp year %s with start date %s and end date %s",
        #     end_date.year,
        #     start_date,
        #     end_date,
        # )

        instance.start_date = datetime.datetime(
            start_date.year, start_date.month, start_date.day
        )
        instance.end_date = datetime.datetime(
            end_date.year, end_date.month, end_date.day
        )
        instance.year = instance.end_date.year

        instance.full_clean()
        instance.save()

        return instance

    def setup_camp_years(self, request=None):
        """
        Checks to see if a camp year for the current calendar year exist.

        Intended for setting up the app, not as an api call.
        """
        current = datetime.date.today()

        # logger.debug("CURRENT: %s", current)

        year = self._get_year(current)

        if not year:
            # logger.debug("Creating CampYear for calendar year %s", current.year)
            return [self._create_year(current)]

        # logger.debug("CampYear for date (%s) already exists: %s", current, year)

        return [year]

