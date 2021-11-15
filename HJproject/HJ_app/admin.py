from django.contrib import admin
from HJ_app.models import SeoulHospital, SeoulHospitalAd
from django.contrib.admin import SimpleListFilter


# Register your models here.
class HospitalFilter(SimpleListFilter):
    title = "승인/미승인"
    parameter_name = "hospital"

    def lookups(self, request, model_admin):
        return[
            ('승인','승인'),
            ('미승인', '미승인'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '승인':
            return queryset.filter(is_confirmed = True)
        elif self.value() == '미승인':
            return queryset.filter(is_confirmed = False)
        else:
            return queryset

@admin.register(SeoulHospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('h_name', 'h_pass', 'h_open', 'h_addr', 'h_tel','h_kind','h_wi', 'h_kung', 'h_url', 'is_confirmed')
    list_editable = ('is_confirmed',)
    list_filter = [HospitalFilter]
    
@admin.register(SeoulHospitalAd)
class HospitalAd_Admin(admin.ModelAdmin):
    list_display = ('h_name', 'h_addr', 'h_tel','h_url', 'h_image', 'h_comment')