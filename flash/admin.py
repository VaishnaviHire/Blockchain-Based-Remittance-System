from django.contrib import admin
from .models import Album
from .models import Song
from .models import Lists
from .models import Position
from .models import Notification, Transfer, AddToWallet
# Register your models here.

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Lists)
admin.site.register(Position)
admin.site.register(Notification)
admin.site.register(Transfer)
admin.site.register(AddToWallet)

