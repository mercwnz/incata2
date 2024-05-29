{ pkgs, lib, config, ... }:

{
  # Including necessary packages
  packages = [
    config.languages.python.package.pkgs.pjsua2
    pkgs.gpsd
  ];

  # Enabling and configuring Python and Poetry
  languages.python = {
    enable = true;
    poetry = {
      enable = true;
      install = {
        enable = true;
        installRootPackage = false;
        onlyInstallRootPackage = false;
        compile = false;
        quiet = false;
        groups = [ ];
        ignoredGroups = [ ];
        onlyGroups = [ ];
        extras = [ ];
        allExtras = false;
        verbosity = "no";
      };
      activate.enable = true;
      package = pkgs.poetry;
    };
  };

  # Adding USB devices to the environment
  hardware = {
    enableAllFirmware = true;

    usb = {
      enable = true;
      # Optional: Specify specific USB devices by vendor and product ID
      # extraConfig = ''
      #   options usbhid quirks=0x1234:0xabcd:0x4
      # '';
    };
  };

  # Additional configuration for hardware, if needed
  boot = {
    kernelModules = [ "usbcore" "usb_storage" "usbhid" ];
  };

  # Optional: Additional services or configurations
  services.udev.extraRules = ''
    # Example rule to add specific permissions for a USB device
    SUBSYSTEM=="usb", ATTR{idVendor}=="1234", ATTR{idProduct}=="abcd", MODE="0666"
  '';
}
