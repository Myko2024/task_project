from django.urls import path

from .views import (MarkMessageAsReadView, MessageCreateView, MessageListView,
                    ThreadCreateView, ThreadDeleteView, ThreadListView,
                    UnreadMessagesCountView, UserListView)

urlpatterns = [
    path("threads/", ThreadCreateView.as_view(), name="thread-create"),
    path("threads/list/", ThreadListView.as_view(), name="thread-list"),
    path("threads/delete/<int:pk>/", ThreadDeleteView.as_view(), name="thread-delete"),
    path("messages/", MessageCreateView.as_view(), name="message-create"),
    path(
        "messages/list/<int:thread_id>/", MessageListView.as_view(), name="message-list"
    ),
    path(
        "messages/read/<int:pk>/",
        MarkMessageAsReadView.as_view(),
        name="mark-message-as-read",
    ),
    path(
        "messages/unread-count/",
        UnreadMessagesCountView.as_view(),
        name="unread-messages-count",
    ),
    path("users/", UserListView.as_view(), name="user-list"),
]
