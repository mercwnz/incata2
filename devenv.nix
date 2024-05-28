{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.11";
    devenv.url = "github:cachix/devenv";
  };

  outputs = { self, nixpkgs, devenv, ... }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in
    devenv.lib.mkDevEnv {
      name = "my-dev-env";

      languages.python = {
        enable = true;
        version = "3.10";
        venv = {
          enable = true;
          requirements = ''
            pyserial
            gps3
            obd
          '';
        };
      };

      packages = [
        pkgs.git
      ];

      shellHook = ''
        export GREET="devenv"
        echo "Environment variable GREET is set to $GREET"
        echo "Python version: $(python -V)"
        echo "Git version: $(git --version)"
        cat << "EOF"
        _______  ________  ________  ________  ________  ________
      _╱       ╲╱        ╲╱    ╱   ╲╱        ╲╱    ╱   ╲╱    ╱   ╲
     ╱         ╱         ╱         ╱         ╱         ╱         ╱
    ╱         ╱        _╱╲        ╱        _╱         ╱╲        ╱
    ╲________╱╲________╱  ╲______╱╲________╱╲__╱_____╱  ╲______╱
    EOF

        echo "Running tests"
        git --version | grep "2.42.0"
      '';
    };
}
