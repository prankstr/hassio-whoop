"""Config flow for WHOOP integration."""

import logging
from typing import Any, Dict, Mapping

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.config_entry_oauth2_flow import LocalOAuth2Implementation

from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN, SCOPES

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class WhoopConfigFlow(config_entry_oauth2_flow.AbstractOAuth2FlowHandler):
    """Handle a config flow for WHOOP."""

    VERSION = 1
    DOMAIN = DOMAIN
    OAUTH2_CLIENT_NAME = "WHOOP"

    @property
    def flow_implementation(
        self,
    ) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
        """Return the OAuth2 implementation details for WHOOP."""
        _LOGGER.debug("Providing flow_implementation for WHOOP config flow")
        return LocalOAuth2Implementation(
            self.hass,
            self.DOMAIN,
            "dummy_client_id_for_form",
            "dummy_client_secret_for_form",
            OAUTH2_AUTHORIZE,
            OAUTH2_TOKEN,
            " ".join(SCOPES),
        )

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return _LOGGER

    @property
    def extra_authorize_data(self) -> Dict[str, Any]:
        """Ensure 'offline_access' is requested for refresh token capability."""
        current_scopes = list(SCOPES)
        if "offline_access" not in current_scopes:
            current_scopes.append("offline")

        data_to_send = {"scope": " ".join(current_scopes)}

        return data_to_send

    async def async_step_user(
        self, user_input: Dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _LOGGER.debug("WHOOP async_step_user, input: %s", user_input is not None)
        return await super().async_step_user(user_input)

    async def async_oauth_create_entry(self, data: Dict[str, Any]) -> ConfigFlowResult:
        """Create an entry for the flow after successful OAuth."""
        _LOGGER.info("WHOOP OAuth successful, creating config entry")
        return self.async_create_entry(title=self.OAUTH2_CLIENT_NAME, data=data)

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an API authentication error or explicit request."""
        _LOGGER.info(
            "[%s] Starting reauthentication flow based on entry_data: %s",
            self.handler,
            entry_data,
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: Dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauth dialog."""
        if user_input is None:
            _LOGGER.debug("[%s] Showing reauth_confirm form.", self.handler)
            return self.async_show_form(step_id="reauth_confirm")

        return await self.async_step_user()
