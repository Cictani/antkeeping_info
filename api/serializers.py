"""Serializer module for api app."""
import rest_framework.serializers as serializers
from drf_extra_fields.fields import IntegerRangeField

import ants.models as ant_models


class SubFamilySerializer(serializers.ModelSerializer):
    """Serializer for a sub family object."""
    class Meta:
        model = ant_models.SubFamily
        fields = ('id', 'name')
        read_only_fields = fields


class GenusNameSerializer(serializers.ModelSerializer):
    """Serializer for a list of genera with only id and name."""
    class Meta:
        model = ant_models.Genus
        fields = ('id', 'name')
        read_only_fields = fields


class GenusSerializer(serializers.ModelSerializer):
    """Serializer for a genus object."""
    sub_family = SubFamilySerializer(many=False, read_only=True)

    class Meta:
        model = ant_models.Genus
        fields = ('id', 'name', 'sub_family')
        read_only_fields = fields


class CommonNamesSerializer(serializers.ModelSerializer):
    """Serializer for a list of common names."""
    language = serializers.SerializerMethodField()

    def get_language(self, obj):
        return obj.get_language_display()

    class Meta:
        model = ant_models.CommonName
        fields = ('language', 'name')
        read_online_fields = fields


class InvalidNamesSerializer(serializers.ModelSerializer):
    """Serializer for a list of invalid names."""
    class Meta:
        model = ant_models.InvalidName
        fields = ('name',)
        read_only_fields = fields


class RegionSerializer(serializers.ModelSerializer):
    """Serializer for a region."""
    class Meta:
        model = ant_models.AntRegion
        fields = ('id', 'name', 'slug', 'type', 'code', 'parent')
        read_only_fields = fields


class RegionListSerializer(serializers.ModelSerializer):
    """Serializer for a list of regions."""
    class Meta:
        model = ant_models.AntRegion
        fields = ('id', 'name', 'slug', 'type')
        read_only_fields = fields


class DistributionForAntSerializer(serializers.ModelSerializer):
    """
        Serializer for a list of distribution object. This serializer
        should be used as part of a serialized ant objects, so all
        the ant specific fields aren't included.
    """
    region = RegionListSerializer(many=False, read_only=True)

    class Meta:
        model = ant_models.Distribution
        fields = ('region',)
        read_only_fields = fields


class AntSpeciesDetailSerializer(serializers.ModelSerializer):
    """Serializer for details of a specific ant."""
    genus = GenusSerializer(many=False, read_only=True)
    common_names = CommonNamesSerializer(many=True, read_only=True)
    invalid_names = InvalidNamesSerializer(many=True, read_only=True)
    distribution = DistributionForAntSerializer(many=True, read_only=True)
    colony_structure = serializers.SerializerMethodField()
    founding = serializers.SerializerMethodField()
    flight_climate = serializers.SerializerMethodField()
    hibernation = serializers.SerializerMethodField()
    nutrition = serializers.SerializerMethodField()

    def get_colony_structure(self, obj):
        return obj.get_colony_structure_display()

    def get_flight_climate(self, obj):
        return obj.get_flight_climate_display()

    def get_founding(self, obj):
        return obj.get_founding_display()

    def get_hibernation(self, obj):
        return obj.get_hibernation_display()

    def get_nutrition(self, obj):
        return obj.get_nutrition_display()

    class Meta:
        model = ant_models.AntSpecies
        exclude = ('ordering',)


class AntsWithNuptialFlightsListSerializer(serializers.ModelSerializer):
    """Serializer for a list of ants with nuptial flight months."""
    class Meta:
        model = ant_models.AntSpecies
        flight_hour_range = IntegerRangeField(source='flight_hour_range')
        fields = ('id', 'name', 'flight_months',
                  'flight_climate', 'flight_hour_range')
        read_only_fields = fields


class AntListSerializer(serializers.ModelSerializer):
    """Serializer for a list of ants."""
    class Meta:
        model = ant_models.AntSpecies
        fields = (
            'id', 'name', 'distribution__native', 'distribution__protected',
            'distribution__red_llist_status'
        )
        read_only_fields = fields


class AntSpeciesNameSerializer(serializers.ModelSerializer):
    """Serializer for a list of ants with only id and name."""
    class Meta:
        model = ant_models.AntSpecies
        fields = (
            'id', 'name'
        )
        read_only_fields = fields
