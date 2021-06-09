import logging
from datetime import datetime
from typing import Optional, List

from pymongo.collection import Collection

from niched.models.schema.groups import GroupDataDB, NewGroupIn, NewGroupMemberIn

logger = logging.getLogger(__name__)


class GroupException(Exception):
    """Exceptions thrown when executing group methods """


class MemberAlreadyExist(GroupException):
    """UserID is already member or owner"""


def check_group_id_exist(groups: Collection, group_id: str) -> bool:
    return groups.count_documents({"group_id": group_id}) > 0


def create_group(groups: Collection, group_details: NewGroupIn) -> bool:
    group_data_insert = GroupDataDB(
        **group_details.dict(),
        members=[],
        creation_date=datetime.utcnow()
    )

    group_dict = group_data_insert.dict()

    try:
        groups.insert_one(group_dict)
        logger.info(f"Group {group_details.name} created successfully!")
        return True
    except Exception as e:
        logger.error(f"Cannot create group {group_details.name}, exception raised {e}")
        return False


def get_group(groups: Collection, group_id: str) -> Optional[GroupDataDB]:
    try:
        group_json = groups.find_one({"group_id": group_id})
        return GroupDataDB(**group_json) if group_json else None
    except Exception as e:
        logger.error(f"Exception raised when fetching group {group_id}: {e}")
        return None


def get_all_groups_in_db(groups: Collection) -> List[GroupDataDB]:
    try:
        groups = groups.find({})
        return [group for group in groups]
    except Exception as e:
        logger.error(f"Exception raised when fetching all groups in database {e} ")
        return []


def group_add_new_member(groups: Collection, users: Collection, group_id: str,
                         new_member: NewGroupMemberIn) -> bool:
    group_json = groups.find_one({"group_id": group_id})
    group_db = GroupDataDB(**group_json)

    if new_member.user_name in group_db.members or new_member.user_name == group_db.author_id:
        raise MemberAlreadyExist("User is already part of this group")

    group_update_res = groups.update_one({"group_id": group_id}, {"$push": {"members": new_member.user_name}})
    if group_update_res.modified_count == 0:
        return False

    users_json = users.update_one({"user_name": new_member.user_name}, {"$push": {"subscribed_groups": group_id}})
    if users_json.modified_count == 0:
        groups.update_one({"group_id": group_id}, {"pull": {"members": new_member.user_name}})
        return False

    return True
