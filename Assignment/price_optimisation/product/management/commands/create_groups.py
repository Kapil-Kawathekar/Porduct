from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = "Create admin and viewer groups with permissions"

    def handle(self, *args, **kwargs):
        # Create groups
        admin_group, _ = Group.objects.get_or_create(name='admin')
        viewer_group, _ = Group.objects.get_or_create(name='viewer')
        viewer_group, _ = Group.objects.get_or_create(name='supplier')

        # Replace 'your_app_name' and 'product' with your actual app and model names
        content_type = ContentType.objects.get(app_label='product', model='product')

        # Assign all permissions to admin
        permissions = Permission.objects.filter(content_type=content_type)
        admin_group.permissions.set(permissions)

        # Assign view-only permission to viewer
        view_permission = Permission.objects.get(codename='view_product', content_type=content_type)
        viewer_group.permissions.add(view_permission)

        self.stdout.write("Groups and permissions created successfully!")
