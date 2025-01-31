from django.db import models
import uuid

# TODO make all contacts into mobile numbers or emails?


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    group_relation = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True) # if groups want to belong together TODO make better abstraction
    contact = models.CharField(max_length=128)
    name = models.CharField(max_length=1024)
    wish_city = models.CharField(max_length=1024)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Refugee(models.Model):
    GENDER_DIVERSE='D'
    GENDER_FEMALE='F'
    GENDER_MALE='M'
    GENDER_UNKNOWN='U'
    GENDER_CHOICES = [
        (GENDER_DIVERSE, 'Diverse'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male'),
        (GENDER_UNKNOWN, 'Unknown'),
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=1024, blank=True)
    last_name = models.CharField(max_length=1024, blank=True)
    age = models.IntegerField(default=40)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNKNOWN,
    )
    contact_data = models.CharField(max_length=1024, blank=True)
    origin = models.CharField(max_length=1024, blank=True)
    origin_checked = models.BooleanField(default=False)
    group = models.ForeignKey(Group, related_name='refugees', on_delete=models.CASCADE)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Flat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    rooms = models.IntegerField(default=1)
    kitchen = models.IntegerField(default=1)
    shared_kitchen = models.BooleanField(default=True)
    shared_bath = models.BooleanField(default=True)
    bath = models.IntegerField(default=1)
    owner_first_name = models.CharField(max_length=1024)
    owner_last_name = models.CharField(max_length=1024)
    contact_data = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    max_male = models.IntegerField(default=0)
    max_kids = models.IntegerField(default=0)
    max_adults = models.IntegerField(default=0)
    min_kids_age = models.IntegerField(default=0)
    max_kids_age = models.IntegerField(default=18)
    interim = models.BooleanField(default=True)

    class Meta:
        ordering = ['rooms']

    def __str__(self):
        return f'{self.rooms}:{self.kitchen}:{self.bath} {self.max_adults}:{self.max_kids} {self.address}'


class Driver(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=1024)
    contact_data = models.CharField(max_length=128)
    car = models.CharField(max_length=128)
    seats = models.IntegerField(default=1)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Notifier(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=1024)
    contact = models.CharField(max_length=128)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Trip(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_location = models.CharField(max_length=1024)
    end_location = models.CharField(max_length=1024)
    end_flat = models.ForeignKey(Flat, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f'{self.start_date} -> {self.end_date}'


class Booking(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f'{self.start_date} -> {self.end_date}'
