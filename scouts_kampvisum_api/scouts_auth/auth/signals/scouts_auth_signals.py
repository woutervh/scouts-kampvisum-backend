from django import dispatch

app_ready = dispatch.Signal()
authenticated = dispatch.Signal()
refreshed = dispatch.Signal()
