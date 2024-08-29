from django.contrib.auth.models import User
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message, Thread
from .serializers import MessageSerializer, ThreadSerializer, UserSerializer


class ThreadCreateView(generics.CreateAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])
        if len(participants) != 2:
            return Response(
                {"error": "Thread must have exactly 2 participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user1, user2 = participants
        if user1 == user2:
            return Response(
                {"error": "Thread must have 2 different participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        thread = (
            Thread.objects.filter(participants=user1)
            .filter(participants=user2)
            .distinct()
        )
        if thread.exists():
            return Response(ThreadSerializer(thread.first()).data)
        return super().post(request, *args, **kwargs)


class ThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Thread.objects.filter(participants=self.request.user)


class ThreadDeleteView(generics.DestroyAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]
    queryset = Thread.objects.all()

    def delete(self, request, *args, **kwargs):
        thread = self.get_object()

        if request.user not in thread.participants.all() and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to delete this thread."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().delete(request, *args, **kwargs)


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        thread = serializer.validated_data["thread"]
        if self.request.user not in thread.participants.all():
            raise serializers.ValidationError(
                "You are not a participant of this thread."
            )
        serializer.save(sender=self.request.user)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        thread_id = self.kwargs["thread_id"]
        return Message.objects.filter(thread_id=thread_id)


class MarkMessageAsReadView(generics.UpdateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(id=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user not in message.thread.participants.all():
            return Response(
                {"error": "You are not allowed to update this message."},
                status=status.HTTP_403_FORBIDDEN,
            )
        message.is_read = True
        message.save()
        return Response(self.get_serializer(message).data)


class UnreadMessagesCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        count = Message.objects.filter(
            thread__participants=request.user, is_read=False
        ).count()
        return Response({"unread_count": count})


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
