"""
    This module contains all models for ants app.
"""
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator, \
    ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from regions.models import Region
from ants.managers import AntRegionManager, CountryAntRegionManager, \
    AntSizeManager, AntSpeciesManager, GenusManager, StateAntRegionManager


# Create your models here.
NO_INFORMATION = _('No information.')

LANG_CHOICES = sorted(
    [(lang_code, _(lang_name)) for lang_code, lang_name in settings.LANGUAGES],
    key=lambda language: language[1])


class SpeciesDescription(models.Model):
    """A textual description of an ant species"""
    language = models.CharField(max_length=7, choices=LANG_CHOICES)
    description = models.TextField()
    species = models.ForeignKey('Species', on_delete=models.CASCADE)


class TaxonomicRankMeta:
    """Base meta class for all Taxonomic rank models"""
    ordering = ['name']


class TaxonomicRank(models.Model):
    """
        Abstract base class for all taxonomic rank models.
    """
    name = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        validators=[
            RegexValidator('^[A-Z][a-z]+$')
        ]
    )
    slug = models.SlugField(blank=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super().save(force_insert, force_update, using,
                     update_fields)

    def __str__(self):
        return self.name


class Family(TaxonomicRank):
    """Model which represents a taxonomic rank of type 'Family'."""
    class Meta(TaxonomicRankMeta):
        verbose_name = _('Family')
        verbose_name_plural = _('Families')


class SubFamily(TaxonomicRank):
    """Model which represents a taxonomic rank of type 'Subfamily'."""
    family = models.ForeignKey(
        Family,
        models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta(TaxonomicRankMeta):
        verbose_name = _('Sub Family')
        verbose_name_plural = _('Sub Families')


class Genus(TaxonomicRank):
    """Model which represents a taxonomic rank of type 'Genus'."""
    sub_family = models.ForeignKey(
        SubFamily,
        models.SET_NULL,
        blank=True,
        null=True
    )

    objects = GenusManager()

    class Meta(TaxonomicRankMeta):
        verbose_name_plural = _('Genera')


class AntRegion(Region):
    """
        A model which describes a region in which ants may live.
    """
    objects = AntRegionManager()
    countries = CountryAntRegionManager()
    states = StateAntRegionManager()
    ant_list_complete = models.BooleanField(default=False)


class Distribution(models.Model):
    """
        A model which describes the destribution of an ant species.
    """
    species = models.ForeignKey(
        'Species',
        on_delete=models.CASCADE
    )
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.CASCADE
    )
    native = models.NullBooleanField(
        blank=True,
        null=True,
        verbose_name=_('Native')
    )
    protected = models.NullBooleanField(
        blank=True,
        null=True,
        verbose_name=_('Protected by law')
    )
    LEAST_CONCERN = 'LEAST_CONCERN'
    NEAR_THREATENED = 'NEAR_THREATENED'
    VULNERABLE = 'VULNERABLE'
    ENDANGERED = 'ENDANGERED'
    CRITICALLY_ENDANGERED = 'CRITICALLY_ENDANGERED'
    EXTINCT_IN_WILD = 'EXTINCT_IN_WILD'
    EXTINCT = 'EXTINCT'
    RED_LIST_CHOICES = (
        (LEAST_CONCERN, _('Least Concern')),
        (NEAR_THREATENED, _('Near Threatened')),
        (VULNERABLE, _('Vulnerable')),
        (ENDANGERED, _('Endangered')),
        (CRITICALLY_ENDANGERED, _('Critically Endangered')),
        (EXTINCT_IN_WILD, _('Extinct in the Wild')),
        (EXTINCT, _('Extinct'))
    )
    red_list_status = models.TextField(
        max_length=40,
        blank=True,
        null=True,
        choices=RED_LIST_CHOICES
    )


class Species(TaxonomicRank):
    """Model which represents a taxonomic rank of type 'Species'."""
    name = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        validators=[
            RegexValidator('^[A-Z][a-z]+ [a-z\\.]+$')
        ])
    genus = models.ForeignKey(
        Genus,
        models.SET_NULL,
        blank=True,
        null=True
    )

    @property
    def name_underscore(self):
        """Returns the species name with an underscore instead of a space."""
        return self.name.replace(" ", "_")

    @property
    def common_names(self):
        """Returns query set which contains all common names of the specific species."""
        return self.commonname_set.all()

    @property
    def common_names_str(self):
        """Returns all common names of the specific species seperated by ','."""
        if self.common_names.exists():
            return ', '.join(str(name) for name in self.common_names)
        else:
            return NO_INFORMATION

    class Meta(TaxonomicRankMeta):
        verbose_name = _('Species')
        verbose_name_plural = _('Species')

class SizeField(models.DecimalField):
    """Field which stores the size of an ant."""
    MAX_DIGITS = 6
    MAX_DECIMAL_PLACES = 2
    MIN_SIZE = Decimal('0.01')
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = self.MAX_DIGITS
        kwargs['decimal_places'] = self.MAX_DECIMAL_PLACES
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['validators'] = [
            MinValueValidator(self.MIN_SIZE)
        ]
        super().__init__(*args, **kwargs)


class Month(models.Model):
    """Model which represents a month"""
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return _(self.name)

    class Meta:
        ordering = ['id']


class AntSize(models.Model):
    """Model which stores size information for a specific ant."""
    WORKER = 'WORKER'
    QUEEN = 'QUEEN'
    MALE = 'MALE'
    ANT_TYPE_CHOICES = (
        (WORKER, _('Worker')),
        (QUEEN, _('Queen')),
        (MALE, _('Male')),
    )
    ANT_SIZE_STRINGS = {
        WORKER: _('Worker size'),
        QUEEN: _('Queen size'),
        MALE: _('Male size'),
    }
    type = models.CharField(
        max_length=20,
        db_index=True,
        choices=ANT_TYPE_CHOICES
    )
    minimum = SizeField(verbose_name=_('Minimum (mm)'))
    maximum = SizeField(verbose_name=_('Maximum (mm)'))
    ant_species = models.ForeignKey('AntSpecies', on_delete=models.CASCADE)

    @staticmethod
    def calc_img_width(size):
        """Calculates the image with based on the size."""
        factor = Decimal(1.16959)
        if size:
            return size * factor
        return None

    def minimum_img(self):
        """Returns the width of the image for minimum size."""
        return self.calc_img_width(self.minimum)

    def maximum_img(self):
        """Returns the width of the image for maximum size."""
        return self.calc_img_width(self.maximum)

    def clean(self):
        if self.minimum > self.maximum:
            raise ValidationError(
                _('Minimum size may not be greater than maximum size!')
            )

    def __str__(self):
        return self.ANT_SIZE_STRINGS.get(self.type)

    objects = AntSizeManager()


class AntSpecies(Species):
    """Model of an ant species."""
    # colony
    MONOGYNOUS = 'MONO'
    POLYGYNOUS = 'POLY'
    OLIGOGYNOUS = 'OLIGO'

    COLONY_STRUCTURE_CHOICES = (
        (MONOGYNOUS, _('Monogynous')),
        (OLIGOGYNOUS, _('Oligogynous')),
        (POLYGYNOUS, _('Polygynous'))
    )

    colony_structure = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        choices=COLONY_STRUCTURE_CHOICES,
        verbose_name=_('Colony Structure')
    )

    @property
    def colony_structure_str(self):
        """Returns the colony structure as a string."""
        if self.colony_structure is None:
            return NO_INFORMATION
        else:
            return dict(self.COLONY_STRUCTURE_CHOICES)[self.colony_structure]

    worker_polymorphism = models.NullBooleanField(
        blank=True,
        null=True,
        verbose_name=_('Worker polymorphism')
    )

    flight_months = models.ManyToManyField(
        Month,
        blank=True,
        verbose_name=_('Nuptial flight months'),
    )

    @property
    def flight_months_str(self):
        """Returns the nuptial flight months as a string."""
        if self.flight_months is None:
            return NO_INFORMATION
        else:
            return ', '.join(str(month) for month in self.flight_months.all())

    LEAVES = 'LEAVES'
    LEAVES_TEXT = _('Leaves, grass and other vegetables')
    OMNIVOROUS = 'OMNIVOROUS'
    OMNIVOROUS_TEXT = _('Omnivorous (sugar water, honey, insects, meat, seeds, \
        nuts etc.)')
    SEEDS = 'SEEDS'
    SEEDS_TEXT = _('Mainly seeds and nuts but dead insects and sugar water, \
        honey too.')
    SUGAR_INSECTS = 'SUGAR_INSECTS'
    SUGAR_INSECTS_TEXT = _('Insects, meat, sugar water, honey etc.')

    NUTRITION_CHOICES = (
        (LEAVES, LEAVES_TEXT),
        (OMNIVOROUS, OMNIVOROUS_TEXT),
        (SEEDS, SEEDS_TEXT),
        (SUGAR_INSECTS, SUGAR_INSECTS_TEXT)
    )

    nutrition = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=NUTRITION_CHOICES,
        verbose_name=_('Nutrition')
    )

    objects = AntSpeciesManager()

    class Meta(TaxonomicRankMeta):
        verbose_name = _('Species')
        verbose_name_plural = _('Species')


class CommonName(models.Model):
    """
        Model for a common name of a species in a aspecific
        language.
    """
    name = models.CharField(max_length=200)
    language = models.CharField(max_length=7, choices=LANG_CHOICES)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Common name')
        verbose_name_plural = _('Common names')
        ordering = ['name']

    def __str__(self):
        return '%s (%s)' % (self.name, dict(LANG_CHOICES)[self.language])


class InvalidName(models.Model):
    """Model for an invalid name of a species."""
    name = models.CharField(max_length=200)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Invalid name')
        verbose_name_plural = _('Invalid names')

    def __str__(self):
        return self.name
