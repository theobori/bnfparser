{
  buildPythonPackage,
  setuptools,
  wheel,
  pytestCheckHook,
}:
buildPythonPackage rec {
  pname = "bnfparser";
  version = "0.1.0";
  pyproject = true;

  src = ./.;

  nativeBuildInputs = [
    setuptools
    wheel
  ];

  nativeCheckInputs = [ pytestCheckHook ];
}
