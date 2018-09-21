from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
import api.v1.urls as v1

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),

]
