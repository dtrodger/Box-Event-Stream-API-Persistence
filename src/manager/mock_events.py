import logging
import random
import datetime

import click
from faker import Faker

from src import utils
from src.sql.models.box_event import BoxEventSQLManager
from src.sql import utils as sql_utils


_LOGGER = logging.getLogger(__name__)


EVENT_TYPES = [
    "ACCESS_GRANTED",
    "ACCESS_REVOKED",
    "ADD_DEVICE_ASSOCIATION",
    "ADD_LOGIN_ACTIVITY_DEVICE",
    "ADMIN_LOGIN",
    "APPLICATION_CREATED",
    "APPLICATION_PUBLIC_KEY_ADDED",
    "APPLICATION_PUBLIC_KEY_DELETED",
    "CHANGE_ADMIN_ROLE",
    "CHANGE_FOLDER_PERMISSION",
    "COLLABORATION_ACCEPT",
    "COLLABORATION_EXPIRATION",
    "COLLABORATION_INVITE",
    "COLLABORATION_REMOVE",
    "COLLABORATION_ROLE_CHANGE",
    "COLLAB_ADD_COLLABORATOR",
    "COLLAB_INVITE_COLLABORATOR",
    "COLLAB_REMOVE_COLLABORATOR",
    "COLLAB_ROLE_CHANGE",
    "COMMENT_CREATE",
    "COMMENT_DELETE",
    "CONTENT_WORKFLOW_ABNORMAL_DOWNLOAD_ACTIVITY",
    "CONTENT_WORKFLOW_AUTOMATION_ADD",
    "CONTENT_WORKFLOW_AUTOMATION_DELETE",
    "CONTENT_WORKFLOW_POLICY_ADD",
    "CONTENT_WORKFLOW_SHARING_POLICY_VIOLATION",
    "CONTENT_WORKFLOW_UPLOAD_POLICY_VIOLATION",
    "COPY",
    "DATA_RETENTION_CREATE_RETENTION",
    "DATA_RETENTION_REMOVE_RETENTION",
    "DELETE",
    "DELETE_USER",
    "DEVICE_TRUST_CHECK_FAILED",
    "DOWNLOAD",
    "EDIT",
    "EDIT_USER",
    "EMAIL_ALIAS_CONFIRM",
    "EMAIL_ALIAS_REMOVE",
    "ENABLE_TWO_FACTOR_AUTH",
    "ENTERPRISE_APP_AUTHORIZATION_UPDATE",
    "FAILED_LOGIN",
    "FILE_MARKED_MALICIOUS",
    "FILE_WATERMARKED_DOWNLOAD",
    "GROUP_ADD_ITEM",
    "GROUP_ADD_USER",
    "GROUP_CREATION",
    "GROUP_DELETION",
    "GROUP_EDITED",
    "GROUP_REMOVE_ITEM",
    "GROUP_REMOVE_USER",
    "ITEM_COPY",
    "ITEM_CREATE",
    "ITEM_DOWNLOAD",
    "ITEM_MAKE_CURRENT_VERSION",
    "ITEM_MODIFY",
    "ITEM_MOVE",
    "ITEM_OPEN",
    "ITEM_PREVIEW",
    "ITEM_RENAME",
    "ITEM_SHARED",
    "ITEM_SHARED_CREATE",
    "ITEM_SHARED_UNSHARE",
    "ITEM_SHARED_UPDATE",
    "ITEM_SYNC",
    "ITEM_TRASH",
    "ITEM_UNDELETE_VIA_TRASH",
    "ITEM_UNSYNC",
    "ITEM_UPLOAD",
    "LEGAL_HOLD_ASSIGNMENT_CREATE",
    "LEGAL_HOLD_ASSIGNMENT_DELETE",
    "LEGAL_HOLD_POLICY_CREATE",
    "LEGAL_HOLD_POLICY_DELETE",
    "LEGAL_HOLD_POLICY_UPDATE",
    "LOCK",
    "LOCK_CREATE",
    "LOCK_DESTROY",
    "LOGIN",
    "MASTER_INVITE_ACCEPT",
    "MASTER_INVITE_REJECT",
    "METADATA_INSTANCE_CREATE",
    "METADATA_INSTANCE_DELETE",
    "METADATA_INSTANCE_UPDATE",
    "METADATA_TEMPLATE_CREATE",
    "METADATA_TEMPLATE_DELETE",
    "METADATA_TEMPLATE_UPDATE",
    "MOVE",
    "NEW_USER",
    "PREVIEW",
    "REMOVE_DEVICE_ASSOCIATION",
    "REMOVE_LOGIN_ACTIVITY_DEVICE",
    "RENAME",
    "RETENTION_POLICY_ASSIGNMENT_ADD",
    "SHARE",
    "SHARE_EXPIRATION",
    "SHIELD_ALERT",
    "STORAGE_EXPIRATION",
    "TAG_ITEM_CREATE",
    "TASK_ASSIGNMENT_CREATE",
    "TASK_ASSIGNMENT_DELETE",
    "TASK_ASSIGNMENT_UPDATE",
    "TASK_CREATE",
    "TASK_UPDATE",
    "TERMS_OF_SERVICE_ACCEPT",
    "TERMS_OF_SERVICE_REJECT",
    "UNDELETE",
    "UNLOCK",
    "UNSHARE",
    "UPDATE_COLLABORATION_EXPIRATION",
    "UPDATE_SHARE_EXPIRATION",
    "UPLOAD",
    "USER_AUTHENTICATE_OAUTH2_ACCESS_TOKEN_CREATE",
    "WATERMARK_LABEL_CREATE",
    "WATERMARK_LABEL_DELETE",
]
EVENT_TEMPLATE = {
    "additional_details": {},
    "created_by": {"id": None, "login": None, "name": None, "type": None},
    "event_id": None,
    "event_type": None,
    "session_id": None,
    "source": {"id": None, "login": None, "name": None, "type": None},
    "type": "event",
    "creation_timestamp": None,
}


def mock_users(count):
    fake = Faker()
    users = []
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        name = first_name + " " + last_name
        email = first_name + last_name + "@threeblindmice.com"
        user = [name, email]
        users.append(user)

    return users


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


@click.command()
@click.option(
    "-e", "--env", default="prod", help="env environment alias", type=str,
)
@utils.config_env
def mock_events(env, config):
    sql_utils.configure_connection(config)
    box_event_sql = BoxEventSQLManager(sql_utils.connection)
    users = mock_users(50)
    d1 = datetime.datetime.strptime("07/1/2019 1:30 PM", "%m/%d/%Y %I:%M %p")
    d2 = datetime.datetime.strptime("05/31/2020 1:30 PM", "%m/%d/%Y %I:%M %p")
    for event in EVENT_TYPES:
        for _ in range(random.randrange(1500)):
            user_number = random.randrange(50)
            new_event = EVENT_TEMPLATE.copy()
            new_event["event_type"] = event
            new_event["created_by"]["login"] = users[user_number][1]
            new_event["created_by"]["name"] = users[user_number][0]
            new_event["created_at"] = random_date(d1, d2)
            box_event_sql.insert_box_event_from_dict(new_event)
