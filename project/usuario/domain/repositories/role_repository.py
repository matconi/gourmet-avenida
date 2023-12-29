from django.contrib.auth.models import Group
from typing import List
from usuario.models import User

def get_by_id(id: int) -> Group:
    return Group.objects.get(id=id)

def get_by_ids(ids: List[int]) -> List[Group]:
    return Group.objects.filter(id__in=ids).order_by('id').all()

    return user.groups.all()

def get_customer_by_user(user: User, ids: List[int]) -> List[Group]:
    return user.groups.filter(id__in=ids).all()

def add(user: User, role: Group) -> Group:
    return user.groups.add(role)

def remove(user: User, role: Group) -> Group:
    return user.groups.remove(role)