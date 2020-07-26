from __future__ import annotations

import boxsdk


def configure_box_auth(config: dict) -> boxsdk.JWTAuth:
    box_auth = boxsdk.JWTAuth.from_settings_dictionary(config["box"]["jwt"])
    box_auth.authenticate_instance()

    return box_auth


def configure_box_client(config: dict) -> boxsdk.Client:
    box_auth = configure_box_auth(config)
    client = boxsdk.Client(box_auth)

    return client
