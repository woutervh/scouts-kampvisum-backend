import logging
import datetime

from ..models import CampYear
from apps.groupadmin.api import ScoutsTemporalDetails


logger = logging.getLogger(__name__)


class CampYearService:

    def get_or_create_year(self, date=None):
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

    def _get_year(self, date):
        camp_date = ScoutsTemporalDetails.get_start_of_camp_year(date)
        logger.debug("Start date of camp year for date %s: %s",
                     date, camp_date)
        qs = CampYear.objects.filter(
            start_date__lte=camp_date, end_date__gte=date)
        if qs.count() == 1:
            logger.debug("Found a year: %s", qs[0])
            return qs[0]

        return None

    def _create_year(self, year):
        instance = CampYear()

        instance.start_date = datetime.datetime(year, 9, 1)
        instance.end_date = datetime.datetime(year + 1, 8, 31)
        instance.year = instance.end_date.year

        instance.full_clean()
        instance.save()

        return instance

    # def can_create_camp(self, date):
    #     start = date.year if date.month >= 6 else date.year - 1
    #     logger.debug("Date: %s %s %s - start: %s",
    #                  date, date.year, date.month, start)
    #     end = start + 1

    #     start_date = datetime.datetime(start, 9, 1)
    #     end_date = datetime.datetime(end, 8, 31)

    #     logger.debug("Setting up CampYear '%s' (%s - %s)",
    #                  end, start_date, end_date)

    #     year = CampYear()
    #     year.start_date = start_date
    #     year.end_date = end_date
    #     year.year = end

    #     year.full_clean()
    #     year.save()

    #     return year

    def setup_camp_years(self):
        """
        Checks to see if a camp year for the current calendar year exist.
        """
        current = datetime.date.today()

        year = self._get_year(current)

        if not year:
            logger.debug(
                "Creating CampYear for calendar year %s", current.year)
            return self._create_year(current.year)

        logger.debug(
            "CampYear for date (%s) already exists: %s", current, year)

        return year
