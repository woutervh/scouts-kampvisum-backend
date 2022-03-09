from django import dispatch

app_ready = dispatch.Signal()
oidc_login = dispatch.Signal()
oidc_refresh = dispatch.Signal()
oidc_authenticated = dispatch.Signal()
