{
  buildPythonPackage,
  setuptools,
  wheel,
  pytestCheckHook,
}:
buildPythonPackage {
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
