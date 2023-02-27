import json

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsUserSession, ScoutsGroup, ScoutsFunction

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserSessionSerializer:
    """Serializes a session stored user instance to a string."""

    @staticmethod
    def to_user_session(scouts_user: ScoutsUser) -> str:
        if ScoutsUser is None:
            return ''

        scouts_user.full_clean()
        scouts_user.save()

        data = {}

        data["scouts_groups"] = []
        for scouts_group in scouts_user._scouts_groups:
            data["scouts_groups"].append({
                "group_admin_id": scouts_group.group_admin_id,
                "number": scouts_group.number,
                "name": scouts_group.name,
                "email": scouts_group.email,
                "website": scouts_group.website,
                "parent_group": scouts_group.parent_group,
                "_child_group_names": ",".join([name for name in scouts_group._child_group_names] if scouts_group._child_group_names else ''),
                "type": scouts_group.type,
            })

        data["scouts_functions"] = []
        for scouts_function in scouts_user._scouts_functions:
            data["scouts_functions"].append({
                "group_admin_id": scouts_function.group_admin_id,
                "begin": scouts_function.begin,
                "end": scouts_function.end,
                "scouts_group": scouts_function.scouts_group,
                "code": scouts_function.code,
                "description": scouts_function.description,
                "type": scouts_function.type,
                "max_birth_date": scouts_function.max_birth_date,
                "adjunct": scouts_function.adjunct,
                "is_leader": scouts_function.is_leader,
            })

        return json.dumps(data, default=str)

    @ staticmethod
    def to_scouts_user(session: ScoutsUserSession) -> dict:
        if not session:
            return {}
        logger.debug(f"SESSION: {session}")

        data: dict = json.loads(json.loads(session.data))
        deserialized = {}

        deserialized["scouts_groups"] = []
        for group in data["scouts_groups"]:
            scouts_group = ScoutsGroup()

            scouts_group.group_admin_id = group["group_admin_id"]
            scouts_group.number = group["number"]
            scouts_group.name = group["name"]
            scouts_group.email = group["email"]
            scouts_group.website = group["website"]
            scouts_group.parent_group = group["parent_group"]
            scouts_group._child_group_names = group["_child_group_names"].split(
                ",") if group["_child_group_names"] else []
            scouts_group.type = group["type"]

            deserialized["scouts_groups"].append(scouts_group)

        deserialized["scouts_functions"] = []
        for function in data["scouts_functions"]:
            scouts_function = ScoutsFunction()

            scouts_function.group_admin_id = function["group_admin_id"]
            scouts_function.begin = function["begin"]
            scouts_function.end = function["end"]
            scouts_function.scouts_group = function["scouts_group"]
            scouts_function.code = function["code"]
            scouts_function.description = function["description"]
            scouts_function.type = function["type"]
            scouts_function.max_birth_date = function["max_birth_date"]
            scouts_function.adjunct = function["adjunct"]
            scouts_function.is_leader = function["is_leader"]

            deserialized["scouts_functions"].append(scouts_function)

        return deserialized
