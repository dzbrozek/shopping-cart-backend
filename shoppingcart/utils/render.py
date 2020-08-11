from djangorestframework_camel_case.render import CamelCaseBrowsableAPIRenderer


class FormlessCamelCaseBrowsableAPIRenderer(CamelCaseBrowsableAPIRenderer):
    def show_form_for_method(self, view, method, request, obj):
        return False

    def get_filter_form(self, data, view, request):
        return None
