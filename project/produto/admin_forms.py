from django import forms
from .models import Unit
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class UnitAdminForm(forms.ModelForm):
    def __thumb_new_images(self) -> None:
        if self.initial.get('image_lg') != self.instance.image_lg:
            self.thumb_images()
            
    def thumb_images(self) -> None:
        sizes = {'image_lg': 512, 'image_sm': 216}
        for field_name, size in sizes.items():
            self.__resize_image(field_name, size)

    def __resize_image(self, field_name: str, size: int) -> None:
        inputed_image = self.cleaned_data["image_lg"]

        image = Image.open(inputed_image)
        image.thumbnail((size, size))

        file_io = BytesIO()
        image.save(file_io, format='JPEG')
        self.__save_resized_image(
            inputed_image, field_name, file_io
        )

    def __save_resized_image(self, inputed_image: str, field_name: str, file_io: BytesIO) -> None:
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
        self.__thumb_new_images()
        return super(UnitAdminForm, self).save(*args, **kwargs)
    
    class Meta:
        model = Unit
        fields = '__all__'

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js',
            'js/admin-shared.js',
        )