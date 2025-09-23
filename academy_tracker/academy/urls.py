from django.urls import path
from .views import student_dashboard, task_list, add_or_update_task, delete_task, add_or_update_learningItem, delete_item, learning, learning_item_list, task_list

urlpatterns = [
    path("dashboard/", student_dashboard, name="student_dashboard"),
    path("tasks/", task_list, name="task_list"),
    path("tasks/add/", add_or_update_task, name="add_task"),
    path("tasks/update/<int:pk>/", add_or_update_task, name="update_task"),
    path("tasks/delete/<int:pk>/", delete_task, name="delete_task"),

    path("learnings/", learning, name="learning_list"),              # list view
    path("learnings/add/", add_or_update_learningItem, name="add_learning"),  # add
    path("learnings/update/<int:pk>/", add_or_update_learningItem, name="update_item"),  # update
    path("learnings/delete/<int:pk>/", delete_item, name="delete_item"),  # del

    
    # subject-specific pages
    path("subjects/<int:subject_id>/learning-items/", learning_item_list, name="learning_items"),
    path("subjects/<int:subject_id>/tasks/", task_list, name="tasks"),

]