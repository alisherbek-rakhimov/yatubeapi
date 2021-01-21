from rest_framework import serializers

from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'created']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'author', 'image', 'pub_date', 'comments']
        depth = 1
