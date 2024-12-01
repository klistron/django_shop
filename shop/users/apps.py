from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(create_buyers_group, sender=self)


def create_buyers_group(sender, **kwargs):
    from django.contrib.auth.models import Group
    from django.contrib.auth.models import Permission

    buyers_group, created = Group.objects.get_or_create(name="Покупатели")

    # Получение и назначение разрешений
    permissions = [
        "add_order",
        "view_order",
        "change_order",
        "change_basketitem",
        "delete_basketitem",
        "view_product",
        "view_review",
    ]

    for permission_codename in permissions:
        try:
            permission = Permission.objects.get(codename=permission_codename)
            buyers_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission {permission_codename} does not exist")

    print("Buyers group created and permissions assigned")
