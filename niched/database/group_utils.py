import logging
from datetime import datetime
from typing import Optional, List

from pymongo.collection import Collection

from niched.models.schema.groups import GroupDataDB, NewGroupIn, GroupMemberIn

logger = logging.getLogger(__name__)


class GroupException(Exception):
    """Exceptions thrown when executing group methods """


class InvalidGroupOperation(GroupException):
    """Invalid Operation in Group"""

    def __init__(self, action, message):
        self.action = action
        self.message = message


def check_group_id_exist(groups: Collection, group_id: str) -> bool:
    return groups.count_documents({"group_id": group_id}) > 0


def create_group(groups: Collection, users: Collection, group_details: NewGroupIn) -> bool:
    group_data_insert = GroupDataDB(
        **group_details.dict(),
        members=[group_details.author_id],
        creation_date=datetime.utcnow()
    )

    group_dict = group_data_insert.dict()

    try:
        groups.insert_one(group_dict)
        logger.info(f"Group {group_details.name} created successfully!")
        users.update_one({"user_name": group_details.author_id},
                         {"$push": {"subscribed_groups": group_details.group_id}})
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


def remove_group(groups: Collection, users: Collection, events: Collection, threads: Collection, comments: Collection,
                 group_id: str):
    users.update_many({"subscribed_groups": group_id}, {"$pull": {"subscribed_groups": group_id}})

    threads_to_remove = threads.find({"group_id": group_id})
    for t in threads_to_remove:
        comments.delete_many({"thread_id": str(t['_id'])})
    threads.delete_many({"group_id": group_id})

    events_to_remove = events.find({"group_id": group_id})
    for e in events_to_remove:
        all_members = e['members']['going'] + e['members']['interested']
        users.update_many({"user_name": {"$in": all_members}}, {"$pull": {"events": str(e['_id'])}})
    events.delete_many({"group_id": group_id})

    groups.delete_one({"group_id": group_id})


def get_all_groups_in_db(groups: Collection) -> List[GroupDataDB]:
    try:
        groups = groups.find({})
        return [GroupDataDB(**group) for group in groups]
    except Exception as e:
        logger.error(f"Exception raised when fetching all groups in database {e} ")
        return []


def check_member_in_group(groups: Collection, group_id: str, user_name: str) -> bool:
    """ Precondition: GROUP_ID and USER_ID should be valid """

    group_json = groups.find_one({"group_id": group_id})
    group_db = GroupDataDB(**group_json)
    return user_name in group_db.members


def group_add_new_member(groups: Collection, users: Collection, group_id: str, new_member: GroupMemberIn) -> bool:
    """ Precondition: GROUP_ID and USER_ID should be valid """

    group_update_res = groups.update_one({"group_id": group_id}, {"$push": {"members": new_member.user_name}})
    if group_update_res.modified_count == 0:
        return False

    users_json = users.update_one({"user_name": new_member.user_name}, {"$push": {"subscribed_groups": group_id}})
    if users_json.modified_count == 0:
        groups.update_one({"group_id": group_id}, {"pull": {"members": new_member.user_name}})
        return False

    return True


def group_remove_member(groups: Collection, users: Collection, group_id: str, user: GroupMemberIn) -> bool:
    """ Precondition: GROUP_ID and USER_ID should be valid """

    group_json = groups.find_one({"group_id": group_id})
    group_db = GroupDataDB(**group_json)

    if user.user_name == group_db.author_id:
        raise InvalidGroupOperation(
            action="remove",
            message=f"User @{user.user_name} is the owner of this group. Cannot remove owner from their group!")

    group_update_res = groups.update_one({"group_id": group_id}, {"$pull": {"members": user.user_name}})
    if group_update_res.modified_count == 0:
        return False

    users_json = users.update_one({"user_name": user.user_name}, {"$pull": {"subscribed_groups": group_id}})
    if users_json.modified_count == 0:
        groups.update_one({"group_id": group_id}, {"$pull": {"members": user.user_name}})
        return False

    return True


def find_groups_contain_tags(groups: Collection, targets: List[str], limit: int, skip: int) -> List[GroupDataDB]:
    res = groups.find({"tags": {"$in": targets}}).skip(skip).limit(limit)
    return [GroupDataDB(**g) for g in res]
