from rest_framework import serializers


class PeopleSerializer(serializers.Serializer):

    id = serializers.SerializerMethodField()
    group_admin_id = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    membership_number = serializers.SerializerMethodField()
    customer_number = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    letter_box = serializers.SerializerMethodField()
    postal_code = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    def get_id(self, obj):
        try:
            return obj.id
        except:
            return None

    def get_group_admin_id(self, obj):
        try:
            return obj.group_admin_id
        except:
            return None

    def get_gender(self, obj):
        try:
            return obj.gender
        except:
            return None

    def get_email(self, obj):
        try:
            return obj.email
        except:
            return None

    def get_phone_number(self, obj):
        try:
            return obj.phone_number
        except:
            return obj.personal_data.phone_number

    def get_first_name(self, obj):
        try:
            return obj.first_name
        except Exception:
            return obj.group_admin_data.first_name

    def get_last_name(self, obj):
        try:
            return obj.last_name
        except Exception:
            return obj.group_admin_data.last_name

    def get_birth_date(self, obj):
        try:
            return obj.birth_date
        except Exception:
            return obj.group_admin_data.birth_date

    def get_membership_number(self, obj):
        try:
            return obj.scouts_data.membership_number
        except Exception:
            return None

    def get_customer_number(self, obj):
        try:
            return obj.scouts_data.customer_number
        except Exception:
            return None

    def get_street(self, obj):
        try:
            return obj.street
        except Exception:
            return obj.addresses[0].street

    def get_number(self, obj):
        try:
            return obj.number
        except Exception:
            return obj.addresses[0].number

    def get_letter_box(self, obj):
        try:
            return obj.letter_box
        except Exception:
            return obj.addresses[0].letter_box

    def get_postal_code(self, obj):
        try:
            return obj.postal_code
        except Exception:
            return obj.addresses[0].postal_code

    def get_city(self, obj):
        try:
            return obj.city
        except Exception:
            return obj.addresses[0].city

    def get_is_member(self, obj):
        if self.get_group_admin_id(obj):
            return True
        return False
