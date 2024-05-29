{ pkgs, lib, config, ... }:

{
  packages = [
    # A python dependency outside of poetry.
    config.languages.python.package.pkgs.pjsua2
  ];

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

  # Adding the required buildInputs
  buildInputs = with pkgs; [
    gpsd
    glibc
  ];

  # Optional: A shell hook to inform the user that the environment is set up.
  shellHook = ''
    echo "Development environment with cgps setup."
  '';
}