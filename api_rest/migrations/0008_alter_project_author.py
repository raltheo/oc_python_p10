# Generated by Django 5.0 on 2024-01-31 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "api_rest",
            "0007_contributor_alter_comment_author_alter_issue_author_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_author",
                to="api_rest.contributor",
            ),
        ),
    ]