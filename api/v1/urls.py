from django.conf.urls import url
import api.v1.companies.views as v1_companies_views
import api.v1.CustomAdmin.views as v1_custom_admin_views

app_name = "api/v1"

urlpatterns = [

    # SuperUser
    url(r'' + str(app_name) + '/super-admin-signup/$', v1_custom_admin_views.AdminSignupAPI.as_view(),
        name='super-admin-signup-v1'),

    # Company
    url(r'' + str(app_name) + '/company-signup/$', v1_companies_views.CompanySignupAPI.as_view(),
        name='company-signup-v1'),

    # Company Admin
    url(r'' + str(app_name) + '/company-admin-signup/$', v1_companies_views.CompanyAdminSignupAPI.as_view(),
        name='company-admin-signup-v1'),

    # Employee Signup
    url(r'' + str(app_name) + '/employee-signup/$', v1_companies_views.EmployeeSignupAPI.as_view(),
        name='employee-signup-v1'),

    # Employee Profile Update
    url(r'' + str(app_name) + '/employee-profile-edit/$', v1_companies_views.EmployeeProfileEditAPI.as_view(),
        name='employee-profile-edit-v1'),

    # Employee Remove
    url(r'' + str(app_name) + '/employee-remove/$', v1_companies_views.RemoveEmployeeAPI.as_view(),
        name='employee-remove-v1'),

]
