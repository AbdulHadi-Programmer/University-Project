from django.urls import path
# from .views import student_dashboard, task_list_all, add_or_update_task, delete_task, add_or_update_learningItem, delete_item, learning, learning_item_list, task_list, subject_delete
from .views import *

urlpatterns = [
    path("dashboard/", student_dashboard, name="student_dashboard"),
    path("tasks/", task_list_all, name="task_list"),
    path("tasks/add/", add_or_update_task, name="add_task"),
    path("subjects/<int:subject_id>/tasks/add/", add_or_update_task, name="add_task_subject"),
    
    path("tasks/update/<int:pk>/", add_or_update_task, name="update_task"),
    path("tasks/delete/<int:pk>/", delete_task, name="delete_task"),

    # path("learnings/", learning, name="learning_list"),              # list view
    # path("learnings/add/", add_or_update_learningItem, name="add_learning"),  # add
    # path("learnings/update/<int:pk>/", add_or_update_learningItem, name="update_item"),  # update
    # path("learnings/delete/<int:pk>/", delete_item, name="delete_item"),  # del
    # path("subjects/<int:subject_id>/learning-items/add/", add_or_update_learningItem, name="add_learning_subject"),

    path("learnings/add/", add_or_update_learningItem, name="add_learning"),                    # Dashboard se
    path("subjects/<int:subject_id>/learning-items/add/", add_or_update_learningItem, name="add_learning_subject"),  # Subject page se
    
    path("learnings/update/<int:pk>/", add_or_update_learningItem, name="update_learning"),   # better name
    path("learnings/delete/<int:pk>/", delete_item, name="delete_item"),

    
    # subject-specific pages
    path("subjects/<int:subject_id>/learning-items/", learning_item_list, name="learning_items"),
    path("subjects/<int:subject_id>/tasks/", task_list_by_subject, name="tasks"),
    # subject add or update:
    path("subjects/add-new-subject/", add_or_update__subject, name="add_subject"),
    path("subjects/update-subject/<int:pk>/", add_or_update__subject, name="update_subject"),
    path("subjects/delete-subject/<int:pk>/", subject_delete, name="delete_subject"),


    # Time Table :
    path("timetable/", timetable_list, name="timetable_list"),
    path("timetable/add/", timetable_create, name="timetable_create"),
    path("timetable/<int:pk>/edit/", timetable_update, name="timetable_update"),
    path("timetable/<int:pk>/delete/", timetable_delete, name="timetable_delete"),

]