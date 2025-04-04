# Generated by Django 5.1.6 on 2025-03-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_conversation_message_delete_chathistory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='conversation',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['sent_at']},
        ),
        migrations.AddField(
            model_name='conversation',
            name='mood_end',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='conversation',
            name='mood_start',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='message',
            name='keywords',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='user',
        ),
    ]
