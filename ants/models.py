from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator, \
    ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from tinymce import models as tinymce_models
from regions.models import Country, Region
from ants.managers import AntSizeManager, AntSpeciesManager, GenusManager


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

    def save(self, *args, **kwargs):
        if self.slug is None or not self.slug:
            self.slug = slugify(self.name)
        super(TaxonomicRank, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Family(TaxonomicRank):
    class Meta(TaxonomicRankMeta):
        verbose_name = _('Family')
        verbose_name_plural = _('Families')


class SubFamily(TaxonomicRank):
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
    sub_family = models.ForeignKey(
        SubFamily,
        models.SET_NULL,
        blank=True,
        null=True
    )

    objects = GenusManager()

    class Meta(TaxonomicRankMeta):
        verbose_name_plural = _('Genera')


class Species(TaxonomicRank):
    name = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        validators=[
            RegexValidator('^[A-Z][a-z]+ [a-z\.]+$')
        ])
    genus = models.ForeignKey(
        Genus,
        models.SET_NULL,
        blank=True,
        null=True
    )
    countries = models.ManyToManyField(
        Country,
        blank=True,
        verbose_name=_('Countries')
    )
    regions = models.ManyToManyField(
        Region,
        blank=True,
        verbose_name=_('Regions')
    )

    @property
    def name_underscore(self):
        return self.name.replace(" ", "_")

    @property
    def common_names(self):
        return self.commonname_set.all()

    @property
    def common_names_str(self):
        if self.common_names.exists():
            return ', '.join(str(name) for name in self.common_names)
        else:
            return NO_INFORMATION

    class Meta(TaxonomicRankMeta):
        verbose_name = _('Species')
        verbose_name_plural = _('Species')


def create_size_field(verbose_name):
    SIZE_MAX_DIGITS = 6
    SIZE_MAX_DECIMAL_PLACES = 2
    SIZE_MIN = Decimal('0.01')
    field = models.DecimalField(
        max_digits=SIZE_MAX_DIGITS,
        decimal_places=SIZE_MAX_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(SIZE_MIN)
        ],
        verbose_name=verbose_name
    )
    return field


class Month(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class AntSize(models.Model):
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
    minimum = create_size_field(_('Minimum (mm)'))
    maximum = create_size_field(_('Maximum (mm)'))
    ant_species = models.ForeignKey('AntSpecies', on_delete=models.CASCADE)

    @staticmethod
    def calc_img_width(size):
        factor = Decimal(1.16959)
        if size:
            return size * factor
        else:
            return None

    def minimum_img(self):
        return self.calc_img_width(self.minimum)

    def maximum_img(self):
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
        verbose_name = _('Ant Species')
        verbose_name_plural = _('Ant Species')


class CommonName(models.Model):
    name = models.CharField(max_length=200)
    language = models.CharField(max_length=7, choices=LANG_CHOICES)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Common name')
        verbose_name_plural = _('Common names')
        ordering = ['name']

    def __str__(self):
        return '%s (%s)' % (self.name, dict(LANG_CHOICES)[self.language])


class ObsoleteName(models.Model):
    name = models.CharField(max_length=200)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Obsolete name')
        verbose_name_plural = _('Obsolete names')

    def __str__(self):
        return self.name
