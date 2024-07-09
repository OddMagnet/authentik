# Generated by Django 4.2.6 on 2023-10-28 14:24

from django.apps.registry import Apps
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def set_oobe_flow_authentication(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    from guardian.shortcuts import get_anonymous_user

    Flow = apps.get_model("authentik_flows", "Flow")
    User = apps.get_model("authentik_core", "User")

    db_alias = schema_editor.connection.alias

    users = User.objects.using(db_alias).exclude(username="akadmin")
    try:
        users = users.exclude(pk=get_anonymous_user().pk)

    except Exception:  # nosec
        pass

    if users.exists():
        Flow.objects.using(db_alias).filter(slug="initial-setup").update(
            authentication="require_superuser"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("authentik_flows", "0026_alter_flow_options"),
    ]

    operations = [
        migrations.RunPython(set_oobe_flow_authentication),
        migrations.AlterField(
            model_name="flow",
            name="authentication",
            field=models.TextField(
                choices=[
                    ("none", "None"),
                    ("require_authenticated", "Require Authenticated"),
                    ("require_unauthenticated", "Require Unauthenticated"),
                    ("require_superuser", "Require Superuser"),
                    ("require_outpost", "Require Outpost"),
                ],
                default="none",
                help_text="Required level of authentication and authorization to access a flow.",
            ),
        ),
    ]
