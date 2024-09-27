{
  buildPythonPackage,
  setuptools,
  wheel,
  graphviz,
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

  propagatedBuildInputs = [ graphviz ];

  nativeCheckInputs = [ pytestCheckHook ];

  pythonImportsCheck = [ "bnfparser" ];
}
