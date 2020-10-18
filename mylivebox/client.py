from .entities import (
    DeviceInfo,
    DynDnsHost,
    VoipConfig,
    NmcStatus,
    WanStatus,
    WifiStatus,
    WifiStats,
    IPTVConfig,
    User,
)
from dateutil.parser import parse as parse_date
from typing import Union, Protocol, List, Optional, Dict
from datetime import datetime
import requests
import json
import logging
import socket
import pickle


logger = logging.getLogger("mylivebox")


def _resolve_livebox_url() -> str:
    return 'http://' + socket.gethostbyname("livebox")


class ClientError(RuntimeError):
    pass


class SessionError(ClientError):
    pass


class BasicCredentials(object):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class SessionBase(Protocol):
    def send_request(self,
                     endpoint: str,
                     method: Optional[str] = None,
                     depth: Optional[int] = None,
                     parameters: Optional[Dict] = None):
        pass

    def save(self) -> bytes:
        pass


class Session(SessionBase):
    def __init__(self,
                 http_session: requests.Session,
                 base_url: str,
                 context_id: str):
        self._http_session = http_session
        self._base_url = base_url
        self._context_id = context_id

    @property
    def context_id(self) -> str:
        return self._context_id

    def send_request(self,
                     endpoint: str,
                     method: Optional[str] = None,
                     depth: Optional[int] = None,
                     parameters: Optional[Dict] = None):
        uri = f"{self._base_url}/sysbus/{endpoint.replace('.', '/')}"
        if method is not None:
            uri = f"{uri}:{method}"
        if depth is not None:
            uri = f"{uri}?_restDepth={depth}"
        response = self._http_session.post(
            uri,
            headers={
                "X-Context": self._context_id,
                "X-Prototype-Version": "1.7",
                "Content-Type": "application/x-sah-ws-1-call+json; charset=UTF-8",
                "Accept": "text/javascript"
            },
            data=json.dumps({
                "parameters": parameters or {}
            })
        )
        logger.debug(response.json())
        result = response.json()["result"]
        if "error" in result or "errors" in result:
            raise SessionError(f"'{endpoint}' request failed: {result}")
        return result

    def save(self) -> bytes:
        binary_data = pickle.dumps({
            "http_session": self._http_session,
            "base_url": self._base_url,
            "context_id": self._context_id
        })
        return binary_data

    @staticmethod
    def load(stream: bytes) -> 'Session':
        data = pickle.loads(stream)
        return Session(data["http_session"], data["base_url"], data["context_id"])

    @staticmethod
    def create(username, password, base_url) -> 'Session':
        session = requests.Session()
        auth_response = session.post(
            f"{base_url}/ws",
            data=json.dumps({
                "service": "sah.Device.Information",
                "method": "createContext",
                "parameters": {
                    "applicationName": "so_sdkut",
                    "username": username,
                    "password": password
                }
            }),
            headers={
                'Content-Type': 'application/x-sah-ws-1-call+json',
                'Authorization': 'X-Sah-Login'
            }
        )
        context_id = auth_response.json()["data"]["contextID"]
        return Session(session, base_url, context_id)


SideEffect = None


class Livebox(object):
    def __init__(self,
                 session_source: Union[SessionBase, BasicCredentials],
                 base_url: str = None):
        base_url = base_url
        if isinstance(session_source, Session):
            self._session = session_source
        elif isinstance(session_source, BasicCredentials):
            base_url = base_url or _resolve_livebox_url()
            self._session = Session.create(
                session_source.username,
                session_source.password,
                base_url)
        else:
            raise ClientError("Invalid input: only support Session or Credentials")

    @property
    def session(self) -> Session:
        return self._session

    def reboot(self) -> SideEffect:
        self._session.send_request("NMC", "reboot")

    @property
    def language(self) -> str:
        response = self._session.send_request("UserInterface", "getLanguage")
        return response["status"]

    @property
    def available_languages(self) -> List[str]:
        response = self._session.send_request("UserInterface", "getLanguage")
        return response["data"]["availableLanguages"]

    @language.setter
    def language(self, new_value: str) -> SideEffect:
        self._session.send_request(
            "UserInterface", "setLanguage",
            parameters={"currentLanguage": new_value}
        )

    def ring_phone(self) -> SideEffect:
        self._session.send_request("VoiceService.VoiceApplication", "ring")

    @property
    def users(self) -> List[User]:
        response = self._session.send_request("UserManagement", "getUsers")
        return [User.deserialize(item) for item in response["status"]]

    @property
    def usb_devices(self) -> List[Dict]:
        response = self._session.send_request("USBHosts", "getDevices")
        return response["status"]

    @property
    def devices(self) -> List[Dict]:
        response = self._session.send_request("Devices", "get")
        return response["status"]

    @property
    def device_info(self) -> DeviceInfo:
        response = self._session.send_request("DeviceInfo", "get")
        return DeviceInfo.deserialize(response["status"])

    @property
    def system_time(self) -> datetime:
        response = self._session.send_request("Time", "getTime")
        return parse_date(response["data"]["time"])

    @property
    def utc_time(self) -> datetime:
        response = self._session.send_request("Time", "getUTCTime")
        return parse_date(response["data"]["time"])

    @property
    def time_synchronized(self) -> datetime:
        response = self._session.send_request("Time", "getStatus")
        return response["data"]["status"] == "Synchronized"

    @property
    def ntp_servers(self) -> List[str]:
        response = self._session.send_request("Time", "getNTPServers")
        return [
            s for s in response["data"]["servers"].values()
            if len(s) > 0
        ]

    @property
    def local_timezone(self) -> str:
        response = self._session.send_request("Time", "getLocalTimeZoneName")
        return response["data"]["timezone"]

    @local_timezone.setter
    def local_timezone(self, timezone: str) -> SideEffect:
        self._session.send_request(
            "Time", "setLocalTimeZoneName",
            parameters={
                "timezone": timezone
            })

    @property
    def local_timezone_names(self) -> List[str]:
        response = self._session.send_request("Time", "listLocalTimeZoneNames")
        return response["data"]["timezones"]

    @property
    def pnp_status(self) -> List[str]:
        response = self._session.send_request("PnP", "get")
        return response["status"]

    @property
    def dyndns_services(self) -> List[str]:
        response = self._session.send_request("DynDNS", "getServices")
        return response["status"]

    @property
    def dyndns_hosts(self) -> List[DynDnsHost]:
        response = self._session.send_request("DynDNS", "getHosts")
        return [DynDnsHost.deserialize(item) for item in response["status"]]

    def add_dyndns_host(self,
                        service: str,
                        hostname: str,
                        username: str,
                        password: str) -> SideEffect:
        self._session.send_request(
            "DynDNS", "addHost",
            parameters={
                "service": service,
                "hostname": hostname,
                "username": username,
                "password": password
            }
        )

    def remove_dyndns_host(self, hostname: str) -> SideEffect:
        self._session.send_request(
            "DynDNS", "delHost",
            parameters={
                "hostname": hostname
            }
        )

    @property
    def nmc_status(self) -> NmcStatus:
        response = self._session.send_request("NMC", "get")
        return NmcStatus.deserialize(response["status"])

    @property
    def wan_status(self) -> WanStatus:
        response = self._session.send_request("NMC", "getWANStatus")
        return WanStatus.deserialize(response["data"])

    @property
    def wifi_status(self) -> WifiStatus:
        response = self._session.send_request("NMC.Wifi", "get")
        return WifiStatus.deserialize(response["status"])

    @property
    def wifi_enabled(self) -> bool:
        return self.wifi_status.enable

    @wifi_enabled.setter
    def wifi_enabled(self, enabled: bool) -> SideEffect:
        assert isinstance(enabled, bool)
        self._session.send_request(
            "NMC.Wifi", "set",
            parameters={"Enable": enabled}
        )

    @property
    def wifi_password_displayed(self) -> bool:
        response = self._session.send_request("Screen", "getShowWifiPassword")
        return response["status"]

    @wifi_password_displayed.setter
    def wifi_password_displayed(self, enabled: bool):
        assert isinstance(enabled, bool)
        self._session.send_request(
            "Screen", "setShowWifiPassword",
            parameters={"Enable": enabled}
        )

    @property
    def wifi_stats(self) -> WifiStats:
        response = self._session.send_request("NMC.Wifi", "getStats")
        return WifiStats.deserialize(response["data"])

    @property
    def voip_config(self) -> List[VoipConfig]:
        response = self._session.send_request("NMC", "getVoIPConfig")
        return [VoipConfig.deserialize(item) for item in response["status"]]

    @property
    def iptv_status(self) -> str:
        response = self._session.send_request("NMC.OrangeTV", "getIPTVStatus")
        return response["data"]["IPTVStatus"]

    @property
    def iptv_config(self) -> List[IPTVConfig]:
        response = self._session.send_request("NMC.OrangeTV", "getIPTVConfig")
        return [IPTVConfig.deserialize(item) for item in response["status"]]

    @property
    def iptv_multi_screens(self) -> bool:
        response = self._session.send_request("NMC.OrangeTV", "getIPTVMultiScreens")
        return response["data"]["Enable"]

    @property
    def firewall_level(self) -> str:
        response = self._session.send_request("Firewall", "getFirewallLevel")
        return response["status"]
