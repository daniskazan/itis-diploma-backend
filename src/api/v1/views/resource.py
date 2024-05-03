from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from api.v1.serializers.response.resource import ResourceSerializer
from core.models import Resource, ResourceGroup


class ResourceViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    filter_backends = [filters.SearchFilter]
    search_fields = ["resource_group__name", "name"]
    queryset = Resource.objects.all().prefetch_related("scripts").order_by("id")

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ResourceSerializer
        return ResourceSerializer

    @staticmethod
    def get_available_resource_names() -> list[dict[str, str]]:
        resource_names = ResourceGroup.objects.distinct("name").values("name")
        return resource_names

    @action(methods=["GET"], detail=False)
    def types(self, request: Request):
        data = self.get_available_resource_names()
        return Response(data, status=status.HTTP_200_OK)
