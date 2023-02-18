from rest_framework import serializers


class FibSerializer(serializers.Serializer):
    random_num = serializers.IntegerField()
    fib_result = serializers.IntegerField()
