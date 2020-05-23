def create_role(id: int, name: str, managed=False):
    return {
        'id': int(id),
        'name': str(name),
        'managed': bool(managed)
    }


def create_matched_role(role, created=False) -> tuple:
    return role, created


ROLE_ALPHA = create_role(1, 'alpha')
ROLE_BRAVO = create_role(2, 'bravo')
ROLE_CHARLIE = create_role(3, 'charlie')
ROLE_MIKE = create_role(13, 'mike', True)

ALL_ROLES = [ROLE_ALPHA, ROLE_BRAVO, ROLE_CHARLIE, ROLE_MIKE]
