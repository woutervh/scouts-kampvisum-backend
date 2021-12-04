from datetime import datetime, date


class DateUtils:
    @staticmethod
    def datetime_from_isoformat(datetime_string: str = None) -> datetime:
        if not datetime_string:
            return None
        return datetime.fromisoformat(datetime_string)

    @staticmethod
    def date_from_isoformat(datetime_string: str = None) -> date:
        if not datetime_string:
            return None
        return DateUtils.datetime_from_isoformat(datetime_string).date()
