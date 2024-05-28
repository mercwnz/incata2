{ pkgs ? import <nixpkgs> {} }:

let
  # Define the Python environment with required packages
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    pyserial
    gps3
    obd
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
