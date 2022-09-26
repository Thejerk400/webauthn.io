from django.shortcuts import render

from homepage.const import libraries, demos
from homepage.services import SessionService, CredentialService
from homepage.helpers import transports_to_ui_string, truncate_credential_id_to_ui_string


def index(request):
    """
    Render the homepage
    """
    context = {
        "libraries": libraries,
        "demos": demos,
    }

    session_service = SessionService()
    session_service.start_session(request=request)

    template = "homepage/index.html"
    if session_service.user_is_logged_in(request=request):
        template = "homepage/profile.html"

        username = request.session["username"]
        credential_service = CredentialService()

        user_credentials = credential_service.retrieve_credentials_by_username(username=username)

        context["credentials"] = [
            {
                "id": truncate_credential_id_to_ui_string(cred.id),
                "sign_count": cred.sign_count,
                "is_disc_cred": cred.is_discoverable_credential,
                "transports": transports_to_ui_string(cred.transports or []),
                "device_type": cred.device_type.lower().replace("_", "-"),
                "backed_up": cred.backed_up,
            }
            for cred in user_credentials
        ]

    return render(request, template, context)