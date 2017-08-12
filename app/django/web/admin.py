from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from web.models import Algorithm, Iteration, LoginHistory


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'is_active')
    fields = ('',)
    exclude = ('id',)
    filter_horizontal = ('users',)


@admin.register(Iteration)
class IterationAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_data', 'output_data', 'status_code', 'algorithm', 'user')
    exclude = ('id', 'finished')
    readonly_fields = (
        'algorithm', 'user', 'status_code', 'status_message', 'created_time', 'finished_time', 'input_data',
        'output_data', 'mail_on_completion', 'mailed'
    )
    search_fields = ['user__email']

    def created_time(self, obj):
        return obj.created.strftime('%d.%m.%Y. %H:%M')
    created_time.short_description = _('početak')

    def finished_time(self, obj):
        return obj.finished.strftime('%d.%m.%Y. %H:%M')
    finished_time.short_description = _('završetak')


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'created_time', 'data')
    readonly_fields = ('address', 'data', 'user', 'created_time')
    search_fields = ['user__email']

    def created_time(self, obj):
        return obj.created.strftime('%d.%m.%Y. %H:%M')
    created_time.short_description = _('vrijeme')