from django.contrib.auth.models import Group

def get_by_id(id: int) -> Group:
    return Group.objects.get(id=id)