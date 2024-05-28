{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-21.11.tar.gz") {} }:

let
  pythonEnv = pkgs.python310.withPackages (ps: with ps; [
    ps.pyserial
    ps.gps3
    ps.obd
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pkgs.git
    pythonEnv
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
}
