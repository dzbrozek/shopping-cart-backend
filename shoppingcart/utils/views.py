class ActionConfigViewSetMixin:
    """
    Mixin that provides config per HTTP method rather than per view.
    Useful when you have a view that implements multiple actions and you want to use
    different serializers, permissions or authenticators

    If there's no entry for a method or an option then just fallback to the default handler

    class MyViewSet(ActionConfigViewSetMixin, ViewSet):
        serializer_class = MyDefaultSerializer
        action_config = {
            'list': {
                'authentication_classes': [SessionAuthentication],
                'permission_classes': [IsAuthenticated, IsAdmin],
            },
            'create': {
                'authentication_classes': [TokenAuthentication],
                'permission_classes': [IsAuthenticated],
                'serializer_class': CustomSerializer,
            }
        }
    """

    def get_config(self):
        method = self.request.method.lower()
        if method == "options":
            action = "metadata"
        else:
            action = self.action_map.get(method)

        return self.action_config.get(action, {})

    def get_serializer_class(self):
        serializer_class = self.get_config().get("serializer_class")

        if serializer_class:
            return serializer_class

        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.get_config().get("permission_classes")

        if permission_classes:
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    def get_authenticators(self):
        authentication_classes = self.get_config().get("authentication_classes")

        if authentication_classes:
            return [auth() for auth in authentication_classes]

        return super().get_authenticators()

    def get_renderers(self):
        renderer_classes = self.get_config().get("renderer_classes")

        if renderer_classes:
            return [renderer() for renderer in renderer_classes]

        return super().get_renderers()
