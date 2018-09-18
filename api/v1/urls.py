from django.conf.urls import url
import api.v1.companies.views as v1_companies_views
import api.v1.CustomAdmin.views as v1_custom_admin_views

app_name = "api/v1"

urlpatterns = [

    url(r'' + str(app_name) + '/super-admin-signup/$', v1_custom_admin_views.AdminSignupAPI.as_view(),
        name='super-admin-signup-v1'),

    url(r'' + str(app_name) + '/company-admin-signup/$', v1_companies_views.CompanyAdminSignupAPI.as_view(),
        name='company-admin-signup-v1'),

]
