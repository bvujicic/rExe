from django.contrib import admin

from web.models import Algorithm, Iteration, LoginHistory


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):

    list_display = ('name', 'file')
    exclude = ('id',)


@admin.register(Iteration)
class IterationAdmin(admin.ModelAdmin):

    list_display = ('id', 'input_data', 'output_data', 'status_code', 'algorithm', 'user')
    exclude = ('id',)
    readonly_fields = ('status_code', 'status_message')


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):

    list_display = ('user', 'address', 'created')