{
    description = "ChopChop Backend";

    inputs = {
        nixpkgs.url     = "github:NixOS/nixpkgs/nixos-24.11";
        flake-utils.url = "github:numtide/flake-utils";
    };

    outputs = { self, nixpkgs, flake-utils, ... }:
        flake-utils.lib.eachDefaultSystem (system:
            let
                pkgs = import nixpkgs {
                    inherit system;
                    overlays = [
                        (final: prev: {
                            opencv4 = prev.opencv4.override {
                                enableGtk3 = true;
                                enablePython = true;
                            };
                        })
                    ];
                };
                
                build_tools = with pkgs; [ pkg-config stdenv.cc.cc.lib ];
                
                dependencies = with pkgs.python312Packages; [
                    imutils
                ];

                dev_tools = with pkgs.python312Packages; [
                    bandit

                    python-lsp-server
                    python-lsp-ruff
                    autopep8
                ];

            in { 
                devShells.default = pkgs.mkShell {
                    buildInputs = [ pkgs.opencv4 ] ++ build_tools ++ dependencies ++ dev_tools;
                    shellHook = ''
                        export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
                    '';
                    LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
                };
            }
        );
}
