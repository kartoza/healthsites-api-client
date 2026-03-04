{
  description = "Healthsites API Client - Python library for healthsites.io API";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        python = pkgs.python312;
        pythonPackages = python.pkgs;

        healthsites-client = pythonPackages.buildPythonPackage {
          pname = "healthsites-api-client";
          version = "0.1.0";
          src = ./.;
          format = "pyproject";

          nativeBuildInputs = with pythonPackages; [
            hatchling
          ];

          propagatedBuildInputs = with pythonPackages; [
            httpx
          ];

          checkInputs = with pythonPackages; [
            pytest
            pytest-asyncio
            pytest-cov
            respx
          ];

          pythonImportsCheck = [ "healthsites" ];

          meta = with pkgs.lib; {
            description = "Python client library for the Healthsites.io API v3";
            homepage = "https://github.com/kartoza/healthsites-api-client";
            license = licenses.mit;
            maintainers = [ ];
          };
        };

        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            python
            pythonPackages.pip
            pythonPackages.httpx
            pythonPackages.pytest
            pythonPackages.pytest-asyncio
            pythonPackages.pytest-cov
            pythonPackages.respx
            pythonPackages.black
            pythonPackages.ruff
            pythonPackages.mypy
            pythonPackages.mkdocs
            pythonPackages.mkdocs-material
            pythonPackages.mkdocstrings
            pre-commit
            git
            gh
          ];

          shellHook = ''
            echo "Healthsites API Client Development Environment"
            echo "=============================================="
            echo ""
            echo "Available commands:"
            echo "  nix run .#test      - Run tests"
            echo "  nix run .#lint      - Run linters"
            echo "  nix run .#format    - Format code"
            echo "  nix run .#docs      - Build documentation"
            echo "  nix run .#docs-serve - Serve documentation locally"
            echo ""
            echo "Made with love by Kartoza | https://kartoza.com"
            echo ""

            # Create virtualenv for editable install
            if [ ! -d .venv ]; then
              python -m venv .venv
            fi
            source .venv/bin/activate
            pip install -q -e ".[dev,docs]" 2>/dev/null || true
          '';
        };

      in {
        packages = {
          default = healthsites-client;
          healthsites-client = healthsites-client;
        };

        devShells.default = devShell;

        apps = {
          test = {
            type = "app";
            program = toString (pkgs.writeShellScript "test" ''
              cd ${toString ./.}
              ${python}/bin/python -m pytest tests/ -v
            '');
          };

          lint = {
            type = "app";
            program = toString (pkgs.writeShellScript "lint" ''
              cd ${toString ./.}
              echo "Running ruff..."
              ${pythonPackages.ruff}/bin/ruff check healthsites/ tests/
              echo "Running mypy..."
              ${pythonPackages.mypy}/bin/mypy healthsites/
            '');
          };

          format = {
            type = "app";
            program = toString (pkgs.writeShellScript "format" ''
              cd ${toString ./.}
              echo "Running black..."
              ${pythonPackages.black}/bin/black healthsites/ tests/
              echo "Running ruff fix..."
              ${pythonPackages.ruff}/bin/ruff check --fix healthsites/ tests/
            '');
          };

          docs = {
            type = "app";
            program = toString (pkgs.writeShellScript "docs" ''
              cd ${toString ./.}
              ${pythonPackages.mkdocs}/bin/mkdocs build
            '');
          };

          docs-serve = {
            type = "app";
            program = toString (pkgs.writeShellScript "docs-serve" ''
              cd ${toString ./.}
              ${pythonPackages.mkdocs}/bin/mkdocs serve
            '');
          };
        };
      }
    );
}
