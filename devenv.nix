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

  enterShell = ''
    echo << EOF
    _______  ________  ________  ________  ________  ________ 
  _╱       ╲╱        ╲╱    ╱   ╲╱        ╲╱    ╱   ╲╱    ╱   ╲
 ╱         ╱         ╱         ╱         ╱         ╱         ╱
╱         ╱        _╱╲        ╱        _╱         ╱╲        ╱ 
╲________╱╲________╱  ╲______╱╲________╱╲__╱_____╱  ╲______╱  
  EOF
  '';

}
