from mylivebox.entities import DeviceInfo


def test_deserialize_device_info():
    data = {
        "Manufacturer": "Sagemcom",
        "ManufacturerOUI": "44A61E",
        "ModelName": "SagemcomFast3965_LB2.8",
        "Description": "SagemcomFast3965_LB2.8 Sagemcom fr",
        "ProductClass": "Livebox 3",
        "SerialNumber": "AN2022410620365",
        "HardwareVersion": "SG_LB3_1.2.1",
        "SoftwareVersion": "SG30_sip-fr-6.62.12.1",
        "RescueVersion": "SG30_sip-fr-6.52.18.1",
        "ModemFirmwareVersion": "",
        "EnabledOptions": "",
        "AdditionalHardwareVersion": "",
        "AdditionalSoftwareVersion": "g6-f-sip-fr",
        "SpecVersion": "1.1",
        "ProvisioningCode": "HASH.3222.2827",
        "UpTime": 429086,
        "FirstUseDate": "0001-01-01T00:00:00Z",
        "DeviceLog": "",
        "VendorConfigFileNumberOfEntries": 1,
        "ManufacturerURL": "http://www.sagemcom.com/",
        "Country": "fr",
        "ExternalIPAddress": "1.2.3.4",
        "DeviceStatus": "Up",
        "NumberOfReboots": 7,
        "UpgradeOccurred": False,
        "ResetOccurred": False,
        "RestoreOccurred": False
    }
    device_info = DeviceInfo.deserialize(data)
    assert device_info.manufacturer == "Sagemcom"
    assert device_info.manufacturer_oui == "44A61E"
    assert device_info.model_name == "SagemcomFast3965_LB2.8"
    assert device_info.description == "SagemcomFast3965_LB2.8 Sagemcom fr"
    assert device_info.product_class == "Livebox 3"
    assert device_info.serial_number == "AN2022410620365"
    assert device_info.hardware_version == "SG_LB3_1.2.1"
    assert device_info.software_version == "SG30_sip-fr-6.62.12.1"
    assert device_info.rescue_version == "SG30_sip-fr-6.52.18.1"
    assert device_info.modem_firmware_version == ""
    assert device_info.enabled_options == ""
    assert device_info.additional_hardware_version == ""
    assert device_info.additional_software_version == "g6-f-sip-fr"
    assert device_info.spec_version == "1.1"
    assert device_info.provisioning_code == "HASH.3222.2827"
    assert device_info.uptime == 429086
    assert device_info.first_use_date == "0001-01-01T00:00:00Z"
    assert device_info.device_log == ""
    assert device_info.vendor_config_file_number_of_retries == 1
    assert device_info.manufacturer_url == "http://www.sagemcom.com/"
    assert device_info.country == "fr"
    assert device_info.external_ip_address == "1.2.3.4"
    assert device_info.device_status == "Up"
    assert device_info.number_of_reboots == 7
    assert device_info.upgrade_occurred is False
    assert device_info.reset_occurred is False
    assert device_info.restore_occurred is False
