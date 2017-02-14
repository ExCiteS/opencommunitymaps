"""Tests for models of logger."""

from django.test import TestCase

# import mock

from geokey.projects.tests.model_factories import ProjectFactory
from geokey.categories.tests.model_factories import CategoryFactory
from geokey.subsets.tests.model_factories import SubsetFactory
from geokey.users.tests.model_factories import UserGroupFactory, UserFactory
from geokey.contributions.tests.model_factories import ObservationFactory, CommentFactory

from ..models import LoggerHistory


class LoggerHistoryTest(TestCase):
    ### TESETING USER ####
    
    ### TESETING SUBSETS ####
    def test_log_create_subset(self):
        subset = SubsetFactory.create()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), subset.project.id)
        self.assertEqual(str(log.action_id), 'created')

    def test_log_delete_subset(self):
        subset = SubsetFactory.create()
        subset.delete()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), subset.project.id)
        self.assertEqual(str(log.action_id), 'deleted')

    def test_log_update_subset(self):
        subset = SubsetFactory.create()
        subset.name = 'New subset'
        subset.save()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), subset.project.id)
        self.assertEqual(str(log.action_id), 'updated') 

    ### TESTING PROJECTS ###
    def test_log_crete_project(self):
        project = ProjectFactory.create()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), project.id)
        self.assertEqual(str(log.action_id), 'created') 

    def test_log_deleted_project(self):
        project = ProjectFactory.create()
        project.delete()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), project.id)
        self.assertEqual(str(log.action_id), 'deleted')

    def test_log_update_project_name(self):
        project = ProjectFactory.create()
        project.name = "merda pa tots"
        project.save()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), project.id)
        self.assertEqual(str(log.action_id), 'updated')  
        self.assertEqual(str(log.action), 'Project renamed')

    def test_log_update_project_isprivate(self):
        project = ProjectFactory.create()
        project.everyone_contributes = 'auth'
        project.save()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), project.id)
        self.assertEqual(str(log.action_id), 'updated')  


    ### TESTING CATEGORIES ####

    def test_log_crete_category(self):
        category = CategoryFactory.create()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), category.project.id)
        self.assertEqual(int(log.category_id), category.id)
        self.assertEqual(str(log.action_id), 'created') 

    def test_log_deleted_category(self):
        category = CategoryFactory.create()
        category.delete()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), category.project.id)
        self.assertEqual(int(log.category_id), category.id)
        self.assertEqual(str(log.action_id), 'deleted')

    def test_log_update_category_name(self):
        category = CategoryFactory.create()
        category.name = "merda pa tots"
        category.save()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), category.project.id)
        self.assertEqual(int(log.category_id), category.id)
        self.assertEqual(str(log.action_id), 'updated')  
        self.assertEqual(str(log.action), 'Category renamed')

    def test_log_update_category_status(self):
        category = CategoryFactory.create()
        category.status = 'inactive'
        category.save()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), category.project.id)
        self.assertEqual(int(log.category_id), category.id)
        self.assertEqual(str(log.action_id), 'updated')  
        self.assertEqual(str(log.action), 'Category is inactive')

     ### TESTING USERGROUP ####
    def test_log_craete_usergroup(self):
        usergroup = UserGroupFactory.create()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), usergroup.project.id)
        self.assertEqual(str(log.action_id), 'created')

    def test_log_delete_usergroup(self):
        usergroup = UserGroupFactory.create()
        usergroup.delete()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), usergroup.project.id)
        self.assertEqual(str(log.action_id), 'deleted')

    def test_log_update_usergroup(self):
        usergroup = UserGroupFactory.create()
        usergroup.name = 'Ole ole ole'
        usergroup.save()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), usergroup.project.id)
        self.assertEqual(str(log.action_id), 'updated')

         ### TESTING OBSERVATION ####
    def test_log_craete_observation(self):
        observation = ObservationFactory.create()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), observation.project.id)
        # self.assertEqual(int(log.category_id), observation.category.id)
        self.assertEqual(str(log.action_id), 'created')

    def test_log_delete_observation(self):
        observation = ObservationFactory.create()
        observation.delete()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), observation.project.id)
        # self.assertEqual(int(log.category_id), observation.category.id)
        self.assertEqual(str(log.action_id), 'deleted')

    ### TESTING COMMENTS ####
    def test_log_craete_comment(self):
        comment = CommentFactory.create()

        log = LoggerHistory.objects.last()
        self.assertEqual(int(log.project_id), comment.commentto.category.project.id)
        self.assertEqual(int(log.category_id), comment.commentto.category.id)
        self.assertEqual(str(log.action_id), 'created')

    def test_log_delete_comment(self):
        comment = CommentFactory.create()
        comment.delete()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), comment.commentto.category.project.id)
        self.assertEqual(int(log.category_id), comment.commentto.category.id)
        self.assertEqual(str(log.action_id), 'deleted')

    def test_log_update_comment(self):
        comment = CommentFactory.create()
        comment.review_status = 'resolved'
        comment.save()

        log = LoggerHistory.objects.last()

        self.assertEqual(int(log.project_id), comment.commentto.category.project.id)
        self.assertEqual(int(log.category_id), comment.commentto.category.id)
        self.assertEqual(str(log.action_id), 'updated')