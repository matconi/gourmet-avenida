from django import forms
from .models import Unit
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class UnitAdminForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

    def thumb_images(self):
        if not self.instance.pk or self.initial.get('image_lg') != self.instance.image_lg:
            sizes = {'image_lg': 512, 'image_sm': 216}
            for field_name, size in sizes.items():
                self.__resize_image(field_name, size)

    def __resize_image(self, field_name, size):
        inputed_image = self.cleaned_data["image_lg"]

        image = Image.open(inputed_image)
        image.thumbnail((size, size))

        file_io = BytesIO()
        image.save(file_io, format='JPEG')
        self.__save_resized_image(
            inputed_image, field_name, file_io
        )

    def __save_resized_image(self, inputed_image, field_name, file_io):
        name, suffix = os.path.splitext(str(inputed_image))[0], field_name.split('_')[1]
        file_name = f"{name}-{suffix}.jpg"

        in_memory_file = InMemoryUploadedFile(
            file_io,
            None,
            file_name,
            'image/jpeg',
            file_io.tell,
            None
        )
        setattr(self.instance, field_name, in_memory_file)

    def save(self, *args, **kwargs):
        self.thumb_images()
        return super(UnitAdminForm, self).save(*args, **kwargs)