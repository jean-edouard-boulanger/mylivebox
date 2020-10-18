from typing import Dict, Type, List
from dataclasses import dataclass, field


def split_by(sep):
    def impl(v):
        return v.split(sep)
    return impl


def default_mapper(x):
    return x


def deserialize(entity_type: Type, data: Dict):
    fields = {
        f.name: f.metadata.get("mapper", default_mapper)(data[f.metadata.get("field", f.name)])
        for f in entity_type.__dataclass_fields__.values()
    }
    return entity_type(**fields)


@dataclass
class NmcStatus:
    connection_error: bool = field(metadata={"field": "ConnectionError"})
    defaults_loaded: bool = field(metadata={"field": "DefaultsLoaded"})
    factory_reset_scheduled: bool = field(metadata={"field": "FactoryResetScheduled"})
    iptv_mode: str = field(metadata={"field": "IPTVMode"})
    offer_type: str = field(metadata={"field": "OfferType"})
    provisioning_state: str = field(metadata={"field": "ProvisioningState"})
    run_mode: str = field(metadata={"field": "RunMode"})
    user_name: str = field(metadata={"field": "Username"})
    wan_mode: str = field(metadata={"field": "WanMode"})
    wan_mode_list: List[str] = field(metadata={"field": "WanModeList", "mapper": split_by(";")})

    @staticmethod
    def deserialize(data: Dict) -> 'NmcStatus':
        return deserialize(NmcStatus, data)


@dataclass
class VoipConfig:
    enable: bool = field(metadata={"field": "Enable"})
    encapsulation: str = field(metadata={"field": "Encapsulation"})
    interface: bool = field(metadata={"field": "Interface"})
    interface_id: bool = field(metadata={"field": "InterfaceId"})
    name: bool = field(metadata={"field": "Name"})
    physical_interface: bool = field(metadata={"field": "PhysInterface"})
    protocol: bool = field(metadata={"field": "Protocol"})

    @staticmethod
    def deserialize(data: Dict) -> 'VoipConfig':
        return deserialize(VoipConfig, data)


@dataclass
class DynDnsHost:
    service: str
    hostname: str
    username: str
    password: str
    last_update: str
    status: str
    enable: bool

    @staticmethod
    def deserialize(data: Dict) -> 'DynDnsHost':
        return deserialize(DynDnsHost, data)


@dataclass
class User:
    name: str
    enable: bool
    type: str
    linux_user: bool
    friendly_name: str = field(metadata={"field": "friendlyname"})
    password_state: str = field(metadata={"field": "passwordstate"})
    groups: List[str]

    @staticmethod
    def deserialize(data: Dict) -> 'User':
        return deserialize(User, data)


@dataclass
class IPTVConfig:
    channel_status: bool = field(metadata={"field": "ChannelStatus"})
    channel_type: str = field(metadata={"field": "ChannelType"})
    channel_number: str = field(metadata={"field": "ChannelNumber"})
    channel_flags: str = field(metadata={"field": "ChannelFlags"})

    @staticmethod
    def deserialize(data: Dict) -> 'IPTVConfig':
        return deserialize(IPTVConfig, data)


@dataclass
class WifiStatus:
    enable: bool = field(metadata={"field": "Enable"})
    status: bool = field(metadata={"field": "Status"})
    configuration_mode: bool = field(metadata={"field": "ConfigurationMode"})
    bgn_user_bandwidth: str = field(metadata={"field": "BGNUserBandwidth"})

    @staticmethod
    def deserialize(data: Dict) -> 'WifiStatus':
        return deserialize(WifiStatus, data)


@dataclass
class WifiStats:
    rx_bytes: int = field(metadata={"field": "RxBytes"})
    tx_bytes: int = field(metadata={"field": "TxBytes"})

    @staticmethod
    def deserialize(data: Dict) -> 'WifiStats':
        return deserialize(WifiStats, data)


@dataclass
class WanStatus:
    wan_state: str = field(metadata={"field": "WanState"})
    link_type: str = field(metadata={"field": "LinkType"})
    link_state: str = field(metadata={"field": "LinkState"})
    mac_address: str = field(metadata={"field": "MACAddress"})
    protocol: str = field(metadata={"field": "Protocol"})
    connection_state: str = field(metadata={"field": "ConnectionState"})
    last_connection_error: str = field(metadata={"field": "LastConnectionError"})
    ip_address: str = field(metadata={"field": "IPAddress"})
    dns_servers: List[str] = field(metadata={"field": "DNSServers", "mapper": split_by(",")})
    ipv6_address: str = field(metadata={"field": "IPv6Address"})
    ipv6_delegate_prefix: str = field(metadata={"field": "IPv6DelegatedPrefix"})

    @staticmethod
    def deserialize(data: Dict) -> 'WanStatus':
        return deserialize(WanStatus, data)


@dataclass
class DeviceInfo:
    manufacturer: str = field(metadata={"field": "Manufacturer"})
    manufacturer_oui: str = field(metadata={"field": "ManufacturerOUI"})
    model_name: str = field(metadata={"field": "ModelName"})
    description: str = field(metadata={"field": "Description"})
    product_class: str = field(metadata={"field": "ProductClass"})
    serial_number: str = field(metadata={"field": "SerialNumber"})
    hardware_version: str = field(metadata={"field": "HardwareVersion"})
    software_version: str = field(metadata={"field": "SoftwareVersion"})
    rescue_version: str = field(metadata={"field": "RescueVersion"})
    modem_firmware_version: str = field(metadata={"field": "ModemFirmwareVersion"})
    enabled_options: str = field(metadata={"field": "EnabledOptions"})
    additional_hardware_version: str = field(metadata={"field": "AdditionalHardwareVersion"})
    additional_software_version: str = field(metadata={"field": "AdditionalSoftwareVersion"})
    spec_version: str = field(metadata={"field": "SpecVersion"})
    provisioning_code: str = field(metadata={"field": "ProvisioningCode"})
    uptime: int = field(metadata={"field": "UpTime"})
    first_use_date: str = field(metadata={"field": "FirstUseDate"})
    device_log: str = field(metadata={"field": "DeviceLog"})
    vendor_config_file_number_of_retries: int = field(metadata={"field": "VendorConfigFileNumberOfEntries"})
    manufacturer_url: str = field(metadata={"field": "ManufacturerURL"})
    country: str = field(metadata={"field": "Country"})
    external_ip_address: str = field(metadata={"field": "ExternalIPAddress"})
    device_status: str = field(metadata={"field": "DeviceStatus"})
    number_of_reboots: int = field(metadata={"field": "NumberOfReboots"})
    upgrade_occurred: bool = field(metadata={"field": "UpgradeOccurred"})
    reset_occurred: bool = field(metadata={"field": "ResetOccurred"})
    restore_occurred: bool = field(metadata={"field": "RestoreOccurred"})

    @staticmethod
    def deserialize(data: Dict) -> 'DeviceInfo':
        return deserialize(DeviceInfo, data)
