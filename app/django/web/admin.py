from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from web.models import Algorithm, Iteration, LoginHistory


def purge_files(self, request, queryset):
    pass

purge_files.short_description = 'Izbriši algoritme i počisti file sustav'

@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'is_active', 'created_time')
    fields = ('name', 'file', 'is_active', 'auto_add', 'document', 'source', 'description', 'users', 'created_time')
    exclude = ('id',)
    readonly_fields = ('created_time',)
    filter_horizontal = ('users',)
    actions = (purge_files, )

    def created_time(self, obj):
        return obj.created.strftime('%d.%m.%Y. %H:%M')
    created_time.short_description = 'vrijeme kreiranja'


@admin.register(Iteration)
class IterationAdmin(admin.ModelAdmin):
    list_display = ('id', 'algorithm', 'user', 'input_data', 'output_data', 'status_code', 'created_time', 'finished_time')
    exclude = ('id', 'finished')
    # readonly_fields = (
    #     'algorithm', 'user', 'status_code', 'status_message', 'created_time', 'finished_time', 'input_data',
    #     'output_data', 'mail_on_completion', 'mailed'
    # )
    search_fields = ['user__email']

    def created_time(self, obj):
        return '{:%d.%m.%Y. %H:%M}'.format(obj.created)
        # return obj.created.strftime('%d.%m.%Y. %H:%M')
    created_time.short_description = 'početak'

    def finished_time(self, obj):
        try:
            return '{:%d.%m.%Y. %H:%M}'.format(obj.finished)
            # return obj.finished.strftime('%d.%m.%Y. %H:%M')
        except AttributeError:
            return None

    finished_time.short_description = 'završetak'


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'created_time', 'data')
    readonly_fields = ('address', 'data', 'user', 'created_time')
    search_fields = ['user__email']

    def created_time(self, obj):
        return '{:%d.%m.%Y. %H:%M}'.format(obj.created)
        # return obj.created.strftime('%d.%m.%Y. %H:%M')
    created_time.short_description = 'vrijeme'