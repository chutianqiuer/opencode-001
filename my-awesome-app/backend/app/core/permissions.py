from typing import List, Optional


def check_permission(user_permissions: List[str], required_permission: str) -> bool:
    return required_permission in user_permissions


def check_permissions(
    user_permissions: List[str], required_permissions: List[str], require_all: bool = False
) -> bool:
    if require_all:
        return all(p in user_permissions for p in required_permissions)
    return any(p in user_permissions for p in required_permissions)


def get_permissions_from_menus(menus: List[dict]) -> List[str]:
    permissions = []
    for menu in menus:
        if menu.get("code"):
            permissions.append(menu["code"])
        if menu.get("children"):
            permissions.extend(get_permissions_from_menus(menu["children"]))
    return permissions
