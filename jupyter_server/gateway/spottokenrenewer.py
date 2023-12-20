import typing as ty

import logging
from jupyter_server.gateway.gateway_client import GatewayTokenRenewerBase, GatewayTokenRenewerMeta
import jupyter_server.base.handlers
import jupyter_server.serverapp


class SpotTokenRenewer(GatewayTokenRenewerBase): # type:ignore[misc]

    def get_token(
            self,
            auth_header_key: str,
            auth_scheme: ty.Union[str, None],
            auth_token: str,
            **kwargs: ty.Any,
    ) -> str:
        token = jupyter_server.base.handlers.get_current_token()
        if token is "":
            logging.error("Could not get current request")
            return auth_token

        logging.info("Auth token refreshed")
        return token
