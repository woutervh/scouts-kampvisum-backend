import datetime

from scouts_auth.groupadmin.settings import GroupadminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsTemporalDetails:
    @staticmethod
    def get_start_of_scout_year(date: datetime.date):
        """
        Returns the start date of the scouts year for the given date.

        A scouts year starts on the 1st of September and ends on the 31st of
        August.
        """
        # @TODO make this into a setting
        if date.month < 9:
            return datetime.date(date.year - 1, 9, 1)

        return datetime.date(date.year, 9, 1)

    @staticmethod
    def get_start_of_camp_year(date: datetime.date):
        """
        Returns the start of the scout year based on a limit date for camps.

        A request for a scout year is assumed to mean the next calendar year
        if the current date is later than this limit date.
        The next camp year is assumed to start on the 1st of May.
        """
        epoch = GroupadminSettings.get_camp_registration_epoch_date()
        if date.month < epoch.month:
            return datetime.date(date.year - 1, 9, 1)

        return datetime.date(date.year, 9, 1)

    @staticmethod
    def get_end_of_camp_year(date: datetime.date):
        """
        Returns the start of the scout year based on a limit date for camps.

        A request for a scout year is assumed to mean the next calendar year
        if the current date is later than this limit date.
        The next camp year is assumed to start on the 1st of May.
        """
        epoch = GroupadminSettings.get_camp_registration_epoch_date()
        if date.month >= epoch.month:
            return datetime.date(date.year + 1, 8, 31)

        return datetime.date(date.year, 8, 31)

    @staticmethod
    def get_start_and_end_date_of_camp_year(date: datetime.date):
        return (
            ScoutsTemporalDetails.get_start_of_camp_year(date),
            ScoutsTemporalDetails.get_end_of_camp_year(date),
        )
    
    def get_date_in_camp_year(self, month, day):
        """Returns the correct date in the current camp year for an abstract date with only a month and a day"""
        (
            start_date,
            end_date,
        ) = ScoutsTemporalDetails.get_start_and_end_date_of_camp_year(date)

        if start_date.month < month:
            return 
