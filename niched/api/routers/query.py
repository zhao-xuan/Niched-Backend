import logging
from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import constr

from niched.database.group_utils import find_groups_contain_tags
from niched.database.mongo import conn
from niched.models.schema.groups import GroupDataDB

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[GroupDataDB], name="search:tags")
def search(
        tags: Optional[List[constr(to_lower=True, strip_whitespace=True)]] = Query(
            [],
            title="Tags/Interests",
            description="Tags/Interests used to match against group tags in the database"),
        limit: int = 10,
        skip: int = 0
):
    groups_coll = conn.get_groups_collection()
    return find_groups_contain_tags(groups_coll, tags, limit, skip)
