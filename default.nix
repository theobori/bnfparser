{
  buildPythonPackage,
  setuptools,
  wheel,
  pytestCheckHook,
}:
buildPythonPackage {
  pname = "bnfparser";
  version = "0.1.0";

  src = ./.;

  nativeBuildInputs = [
    setuptools
    wheel
  ];

  nativeCheckInputs = [ pytestCheckHook ];
}
