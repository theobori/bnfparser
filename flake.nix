{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forEachSupportedSystem =
        f: nixpkgs.lib.genAttrs supportedSystems (system: f { pkgs = import nixpkgs { inherit system; }; });
    in
    {
      packages = forEachSupportedSystem (
        { pkgs }:
        {
          default = pkgs.callPackage ./. {
            inherit (pkgs.python3Packages)
              buildPythonPackage
              setuptools
              wheel
              pytestCheckHook
              graphviz
              ;
          };
        }
      );

      devShells = forEachSupportedSystem (
        { pkgs }:
        {
          default = pkgs.mkShell {
            venvDir = ".venv";
            packages =
              with pkgs;
              [
                python3
                graphviz
              ]
              ++ (with pkgs.python3Packages; [
                setuptools
                pip
                venvShellHook
                build
                pytest
                pylint
                graphviz
              ]);
          };
        }
      );
    };
}
