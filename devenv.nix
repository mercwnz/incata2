{ pkgs ? import <nixpkgs> {} }:

let
  # Define the Python environment with required packages
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
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
  '';
}
