{ pkgs, lib, config, inputs, ... }:

{
  env.GREET = "devenv";

  packages = [ pkgs.git ];

  enterShell = ''
    git --version
    python -V
    cat << "EOF"
    _______  ________  ________  ________  ________  ________ 
  _╱       ╲╱        ╲╱    ╱   ╲╱        ╲╱    ╱   ╲╱    ╱   ╲
 ╱         ╱         ╱         ╱         ╱         ╱         ╱
╱         ╱        _╱╲        ╱        _╱         ╱╲        ╱ 
╲________╱╲________╱  ╲______╱╲________╱╲__╱_____╱  ╲______╱  

EOF
  '';

  enterTest = ''
    echo "Running tests"
    git --version | grep "2.42.0"
  '';

  languages.python = {
    enable = true;
    version = "3.12.3";
    venv = {
      enable = true;
      requirements = ''
        pyserial
        gps3
        obd
      '';
    };
  };
}
