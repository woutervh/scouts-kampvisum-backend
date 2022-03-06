from rest_framework import serializers

from apps.visums.models import SubCategory


class SubCategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=128)

    class Meta:
        model = SubCategory
        # fields = "__all__"
        exclude = ["category", "camp_types"]

    def to_internal_value(self, data: dict) -> dict:
        id = data.get("id", None)
        if id:
            instance: SubCategory = SubCategory.objects.safe_get(
                id=id, raise_error=True
            )

            if instance:
                data = {"id": id, "name": instance.name}

        data = super().to_internal_value(data)

        return data

    def validate(self, data: dict) -> SubCategory:
        return SubCategory.objects.safe_get(**data, raise_error=True)
