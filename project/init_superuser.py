from django import setup
from django.conf import settings
from django.contrib.auth import get_user_model
import os

def main():
    os.environ.get('DJANGO_SETTINGS_MODULE') or os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gourmetavenida.settings')
    setup()

    User = get_user_model()
    if User.objects.count() == 0:
        for user in settings.ADMINS:
            first_name, email = user[0], user[1]
            password = 'admin'
            admin = User.objects._create_superuser(email, first_name, password, phone='(12)12345-1234')
            print(f'Created user for {admin.get_short_name()} ({email}).')
    else:
        print("All admin users were created.")
if __name__ == '__main__':
    main()