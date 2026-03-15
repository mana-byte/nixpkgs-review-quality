
def find_line_numbers(file: str, word: str) -> list[int]:
    lines = file.splitlines()
    return [i + 1 for i, line in enumerate(lines) if word in line]

def number_each_line(file: str) -> str:
    lines = file.splitlines()
    return "\n".join(f"{i + 1}: {line}" for i, line in enumerate(lines))


if __name__ == "__main__":
    file_content = """{\n  lib,\n  stdenv,\n  buildPythonPackage,\n  fetchFromGitHub,\n\n  # build-system\n  setuptools,\n\n  # dependencies\n  lap,\n  matplotlib,\n  opencv-python,\n  pandas,\n  pillow,\n  polars,\n  psutil,\n  py-cpuinfo,\n  pyyaml,\n  requests,\n  scipy,\n  seaborn,\n  torch,\n  torchvision,\n  tqdm,\n  ultralytics-thop,\n\n  # tests\n  aiohttp,\n  onnx,\n  onnxruntime,\n  pytestCheckHook,\n}:\n\nbuildPythonPackage rec {\n  pname = "test_pr";\n  version = "8.4.21";\n  pyproject = true;\n\n  src = fetchFromGitHub {\n    owner = "ultralytics";\n    repo = "ultralytics";\n    tag = "v${version}";\n    hash = "sha256-KyTqO5jjYXnw5xwKlvwnY99SE0zkLaz8Ck6hKb7non8=";\n  };\n\n  nativeBuildInputs = [ setuptools ];\n\n  pythonRelaxDeps = [\n    "numpy"\n  ];\n\n  propagatedBuildInputs = [\n    lap\n    matplotlib\n    opencv-python\n    pandas\n    pillow\n    polars\n    psutil\n    py-cpuinfo\n    pyyaml\n    requests\n    scipy\n    scipy\n    seaborn\n    torch\n    torchvision\n    tqdm\n    ultralytics-thop\n  ];\n\n  pythonImportsCheck = [ "ultralytics" ];\n\n  nativeCheckInputs = [\n    aiohttp\n    onnx\n    onnxruntime\n    pytestCheckHook\n  ];\n\n  meta = {\n    homepage = "https://github.com/ultralytics/ultralytics";\n    changelog = "https://github.com/ultralytics/ultralytics/releases/tag/${src.tag}";\n    description = "Train YOLO models for computer vision tasks";\n    mainProgram = "yolo";\n    license = lib.licenses.agpl3Only;\n    maintainers = with lib.maintainers; [\n      no\n    ];\n  };\n}\n"""
    word = "buildPythonPackage"
    line_numbers = find_line_numbers(file_content, word)
    file_numbered = number_each_line(file_content)
    print(line_numbers)
    print(file_numbered)
