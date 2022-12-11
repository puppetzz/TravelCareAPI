from django.db import models


class Country(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class Province(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class District(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class AddressManager(models.Manager):
    def create(self, **kwargs):
        id = kwargs['id']
        country = kwargs['country']
        province = kwargs['province']
        district = kwargs['district']

        print(country)

        address = self.model(
            id=id,
            country=country,
            province=province,
            district=district,
            street_address=kwargs['street_address']
        )
        address.save()
        return address


class Address(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=555)

    objects = AddressManager()
