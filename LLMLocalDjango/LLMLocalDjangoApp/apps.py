from django.apps import AppConfig


class LlmlocaldjangoappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "LLMLocalDjangoApp"

    def ready(self) -> None:
        return super().ready()
