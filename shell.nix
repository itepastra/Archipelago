{ pkgs ? import <nixpkgs> { } }:

let
  pythonEnv = pkgs.python311Full.withPackages(ps: with ps; [ pip virtualenv kivy ]);

in
pkgs.mkShell {
  packages = [
    pythonEnv
  ];
}

