# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 13:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import plaza.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('number', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team_min_size', models.IntegerField(default=1)),
                ('team_max_size', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=128)),
                ('semester', models.CharField(max_length=3)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('max_enroll', models.IntegerField(null=True)),
                ('access_code', models.IntegerField(null=True)),
                ('public', models.BooleanField(default=True)),
                ('instructors', models.ManyToManyField(related_name='courses_managed', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ManyToManyField(related_name='courses_assisted', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(related_name='courses_taken', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('category', models.CharField(choices=[('PDF', 'application/pdf'), ('JPEG', 'image/jpeg'), ('GIF', 'image/gif'), ('MP4', 'video/mp4'), ('EMBED', 'text/html'), ('PNG', 'image/png'), ('CAL', 'text/calendar')], default='0', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MatchMakingPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MatchMakingTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='potential_team', to='plaza.Assignment')),
                ('potential_members', models.ManyToManyField(related_name='potential_team', to='plaza.MatchMakingPerson')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(choices=[('0', ' answered your question'), ('1', ' followed your question'), ('2', ' commented your question'), ('3', ' upvoted your answer'), ('4', ' downvoted your answer'), ('5', ' replied to your comments'), ('6', ' posted a new question in your following tag'), ('7', ' followed you'), ('8', ' add you to a team')], max_length=1)),
                ('extra_content', models.CharField(max_length=256)),
                ('status', models.CharField(choices=[('0', 'unseen'), ('1', 'seen')], default='0', max_length=1)),
                ('destination', models.URLField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=32)),
                ('short_bio', models.CharField(blank=True, max_length=1024, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'N/A')], max_length=1, null=True)),
                ('field', models.CharField(max_length=32)),
                ('institution', models.CharField(max_length=32)),
                ('profile_image', models.ImageField(blank=True, default='profile-photos/user_ico.png', upload_to=plaza.models.profile_image_rename)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('text', tinymce.models.HTMLField()),
                ('parent_id', models.IntegerField(default=0)),
                ('root_id', models.IntegerField(default=0)),
                ('post_type', models.CharField(choices=[('0', 'question'), ('1', 'student_reply'), ('2', 'staff_reply'), ('3', 'comments')], default='0', max_length=1)),
                ('status', models.CharField(choices=[('0', 'resolved'), ('1', 'unresolved'), ('2', 'answered'), ('3', 'unanswered')], default='0', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pinned', models.BooleanField(default=False)),
                ('assignee', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_posts', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='plaza.Person')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='plaza.Course')),
                ('editors', models.ManyToManyField(related_name='edited_posts', to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(related_name='followed_posts', to=settings.AUTH_USER_MODEL)),
                ('readers', models.ManyToManyField(related_name='read_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('notes', models.CharField(max_length=128)),
                ('resource_type', models.CharField(choices=[('P', 'Plain'), ('D', 'Document'), ('V', 'Video'), ('F', 'Folder'), ('N', 'N/A')], max_length=16)),
                ('due', models.DateField(null=True)),
                ('file', models.FileField(upload_to='resources/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='plaza.Course')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='plaza.Resource')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='plaza.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='plaza.Assignment')),
                ('members', models.ManyToManyField(related_name='teams', to='plaza.Person')),
            ],
        ),
        migrations.AddField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(related_name='tag_resources', to='plaza.Tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='tag_posts', to='plaza.Tag'),
        ),
        migrations.AddField(
            model_name='person',
            name='downvotes',
            field=models.ManyToManyField(related_name='downvoters', to='plaza.Post'),
        ),
        migrations.AddField(
            model_name='person',
            name='following',
            field=models.ManyToManyField(related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='person',
            name='upvotes',
            field=models.ManyToManyField(related_name='upvoters', to='plaza.Post'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_received', to='plaza.Person'),
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_sent', to='plaza.Person'),
        ),
        migrations.AddField(
            model_name='matchmakingperson',
            name='confirmed_team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='confirmed_person', to='plaza.MatchMakingTeam'),
        ),
        migrations.AddField(
            model_name='matchmakingperson',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='matchmaking_person', to='plaza.Person'),
        ),
        migrations.AddField(
            model_name='matchmakingperson',
            name='potential_teams',
            field=models.ManyToManyField(related_name='matchmaking_person', to='plaza.MatchMakingTeam'),
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='plaza.Person'),
        ),
        migrations.AddField(
            model_name='item',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='plaza.Post'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='plaza.Course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='tags',
            field=models.ManyToManyField(related_name='tag_assignments', to='plaza.Tag'),
        ),
    ]
