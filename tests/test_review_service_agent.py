"""test require network, agent api key"""

import pytest
from unittest.mock import patch, MagicMock
from quality.agents import AGENTS
from quality.review.services.agent import AgentService
from mistralai.models.sdkerror import SDKError

EXAMPLE_REVIEW_INPUT_1 = {
    "pkgs/development/python-modules/pr_test/package.nix": {
        "content": '1: {\n2:   lib,\n3:   stdenv,\n4:   buildPythonPackage,\n5:   fetchFromGitHub,\n6: \n7:   # build-system\n8:   setuptools,\n9: \n10:   # dependencies\n11:   lap,\n12:   matplotlib,\n13:   opencv-python,\n14:   pandas,\n15:   pillow,\n16:   polars,\n17:   psutil,\n18:   py-cpuinfo,\n19:   pyyaml,\n20:   requests,\n21:   scipy,\n22:   seaborn,\n23:   torch,\n24:   torchvision,\n25:   tqdm,\n26:   ultralytics-thop,\n27: \n28:   # tests\n29:   aiohttp,\n30:   onnx,\n31:   onnxruntime,\n32:   pytestCheckHook,\n33: }:\n34: \n35: buildPythonPackage rec {\n36:   pname = "test_pr";\n37:   version = "8.4.21";\n38:   pyproject = true;\n39: \n40:   src = fetchFromGitHub {\n41:     owner = "ultralytics";\n42:     repo = "ultralytics";\n43:     tag = "v${version}";\n44:     hash = "sha256-KyTqO5jjYXnw5xwKlvwnY99SE0zkLaz8Ck6hKb7non8=";\n45:   };\n46: \n47:   nativeBuildInputs = [ setuptools ];\n48: \n49:   pythonRelaxDeps = [\n50:     "numpy"\n51:   ];\n52: \n53:   propagatedBuildInputs = [\n54:     lap\n55:     matplotlib\n56:     opencv-python\n57:     pandas\n58:     pillow\n59:     polars\n60:     psutil\n61:     py-cpuinfo\n62:     pyyaml\n63:     requests\n64:     scipy\n65:     scipy\n66:     seaborn\n67:     torch\n68:     torchvision\n69:     tqdm\n70:     ultralytics-thop\n71:   ];\n72: \n73:   pythonImportsCheck = [ "ultralytics" ];\n74: \n75:   nativeCheckInputs = [\n76:     aiohttp\n77:     onnx\n78:     onnxruntime\n79:     pytestCheckHook\n80:   ];\n81: \n82:   meta = {\n83:     homepage = "https://github.com/ultralytics/ultralytics";\n84:     changelog = "https://github.com/ultralytics/ultralytics/releases/tag/${src.tag}";\n85:     description = "Train YOLO models for computer vision tasks";\n86:     mainProgram = "yolo";\n87:     license = lib.licenses.agpl3Only;\n88:     maintainers = with lib.maintainers; [\n89:       no\n90:     ];\n91:   };\n92: }',
        "review_points": {
            "finalAttrs": {
                "instructions": "Replace rec with finalAttrs in the builder function without breaking its recursiveness. finalAttrs is a more modern and efficient way to inherit attributes from stdenv in Nix.",
                "examples": [
                    '\n            {\n                "before": "buildPythonPackage rec {"\n                "after": "buildPythonPackage (finalAttrs {"\n                "explanation": "Replaces rec with finalAttrs in the builder function. Reminder to close the parentheses at the end of the builder function. This change allows for more efficient inheritance of attributes from stdenv in Nix, while maintaining the recursive nature of the builder function."\n            }\n            ',
                    '\n            {\n                "before": "tag = "v${version}";"\n                "after": "tag = "v${finalAttrs.version}";"\n                "explanation": "Keep the recursiveness of the builder function while replacing rec with finalAttrs. In this example, we replace version with finalAttrs.version to ensure that the builder function can still access the version attribute from stdenv without breaking its recursiveness."\n            }\n            ',
                    '\n            {\n                "before": "changelog = "https://github.com/holoviz/datashader/blob/${src.tag}/CHANGELOG.rst";"\n                "after": "changelog = "https://github.com/holoviz/datashader/blob/${finalAttrs.src.tag}/CHANGELOG.rst";"\n                "explanation": "Keep the builder function recursive by replacing rec with finalAttrs, which allows to inherit attributes from stdenv in a more modern and efficient way. In this example, we replace src.tag with finalAttrs.src.tag to maintain the recursive nature of the builder function while using finalAttrs for better performance and maintainability."\n            }\n            ',
                ],
            },
            "Modern Python build tools": {
                "instructions": "buildPythonPackage and buildPythonApplication have their own modern way to build a package. Using build-system instead of nativeBuildInputs and dependencies instead of propagatedBuildInputs is now the norm.",
                "examples": [
                    '{ "before": "nativeBuildInputs = [", "after": "build-system = [", "explanation": "According to modern conventions" }',
                    '{ "before": "propagatedBuildInputs = [", "after": "dependencies = [", "explanation": "According to modern conventions" }',
                ],
            },
        },
    }
}

EXAMPLE_REVIEW_INPUT_2 = {
    "pkgs/by-name/mi/mistral-vibe/package.nix": {
        "content": '1: {\n2:   lib,\n3:   stdenv,\n4:   python3Packages,\n5:   fetchFromGitHub,\n6: \n7:   # tests\n8:   uv,\n9:   versionCheckHook,\n10:   writableTmpDirAsHomeHook,\n11: }:\n12: \n13: python3Packages.buildPythonApplication rec {\n14:   pname = "mistral-vibe";\n15:   version = "1.3.3";\n16:   pyproject = true;\n17: \n18:   src = fetchFromGitHub {\n19:     owner = "mistralai";\n20:     repo = "mistral-vibe";\n21:     tag = "v${version}";\n22:     hash = "sha256-nW7pRSyv+t/7yatx84PMgxsHRTfRqqpy6rz+dQfLluU=";\n23:   };\n24: \n25:   build-system = with python3Packages; [\n26:     editables\n27:     hatch-vcs\n28:     hatchling\n29:   ];\n30: \n31:   pythonRelaxDeps = [\n32:     "agent-client-protocol"\n33:     "mistralai"\n34:     "pydantic"\n35:     "pydantic-settings"\n36:     "watchfiles"\n37:   ];\n38:   dependencies = with python3Packages; [\n39:     agent-client-protocol\n40:     aiofiles\n41:     httpx\n42:     mcp\n43:     mistralai\n44:     packaging\n45:     pexpect\n46:     pydantic\n47:     pydantic-settings\n48:     pyperclip\n49:     python-dotenv\n50:     pyyaml\n51:     rich\n52:     textual\n53:     textual-speedups\n54:     tomli-w\n55:     watchfiles\n56:   ];\n57: \n58:   pythonImportsCheck = [ "vibe" ];\n59: \n60:   nativeCheckInputs = [\n61:     python3Packages.pytest-asyncio\n62:     python3Packages.pytest-textual-snapshot\n63:     python3Packages.pytest-xdist\n64:     python3Packages.pytestCheckHook\n65:     python3Packages.respx\n66:     uv\n67:     versionCheckHook\n68:     writableTmpDirAsHomeHook\n69:   ];\n70:   versionCheckProgramArg = "--version";\n71:   versionCheckKeepEnvironment = [ "HOME" ];\n72:   pytestFlags = [ "tests/cli/test_clipboard.py" ];\n73: \n74:   disabledTests = [\n75:     # AssertionError: assert \'/nix/store/rlq03x4cwf8zn73hxaxnx0zn5q9kifls-bash-5.3p3/bin/sh:\n76:     # warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8): No such file or directory\\n\' == \'\'\n77:     "test_decodes_non_utf8_bytes"\n78:     "test_runs_echo_successfully"\n79:     "test_truncates_output_to_max_bytes"\n80:   ]\n81:   ++ lib.optionals stdenv.hostPlatform.isDarwin [\n82:     # AssertionError: assert 3 == 4\n83:     "test_get_copy_fns_with_wl_copy"\n84:     "test_get_copy_fns_with_both_system_tools"\n85:     "test_get_copy_fns_with_xclip"\n86:   ];\n87: \n88:   disabledTestPaths = [\n89:     # All snapshot tests fail with AssertionError\n90:     "tests/snapshots/"\n91: \n92:     # ACP tests require network access\n93:     "tests/acp/test_acp.py"\n94:   ];\n95: \n96:   meta = {\n97:     description = "Minimal CLI coding agent by Mistral";\n98:     homepage = "https://github.com/mistralai/mistral-vibe";\n99:     changelog = "https://github.com/mistralai/mistral-vibe/blob/${src.tag}/CHANGELOG.md";\n100:     license = lib.licenses.asl20;\n101:     maintainers = with lib.maintainers; [\n102:       GaetanLepage\n103:       shikanime\n104:     ];\n105:     mainProgram = "vibe";\n106:   };\n107: }',
        "review_points": {
            "finalAttrs": {
                "instructions": "Replace rec with finalAttrs in the builder function without breaking its recursiveness. finalAttrs is a more modern and efficient way to inherit attributes from stdenv in Nix.",
                "examples": [
                    '\n            {\n                "before": "buildPythonPackage rec {"\n                "after": "buildPythonPackage (finalAttrs {"\n                "explanation": "Replaces rec with finalAttrs in the builder function. Reminder to close the parentheses at the end of the builder function. This change allows for more efficient inheritance of attributes from stdenv in Nix, while maintaining the recursive nature of the builder function."\n            }\n            ',
                    '\n            {\n                "before": "tag = "v${version}";"\n                "after": "tag = "v${finalAttrs.version}";"\n                "explanation": "Keep the recursiveness of the builder function while replacing rec with finalAttrs. In this example, we replace version with finalAttrs.version to ensure that the builder function can still access the version attribute from stdenv without breaking its recursiveness."\n            }\n            ',
                    '\n            {\n                "before": "changelog = "https://github.com/holoviz/datashader/blob/${src.tag}/CHANGELOG.rst";"\n                "after": "changelog = "https://github.com/holoviz/datashader/blob/${finalAttrs.src.tag}/CHANGELOG.rst";"\n                "explanation": "Keep the builder function recursive by replacing rec with finalAttrs, which allows to inherit attributes from stdenv in a more modern and efficient way. In this example, we replace src.tag with finalAttrs.src.tag to maintain the recursive nature of the builder function while using finalAttrs for better performance and maintainability."\n            }\n            ',
                ],
            },
            "Modern Python build tools": {
                "instructions": "buildPythonPackage and buildPythonApplication have their own modern way to build a package. Using build-system instead of nativeBuildInputs and dependencies instead of propagatedBuildInputs is now the norm.",
                "examples": [
                    '{ "before": "nativeBuildInputs = [", "after": "build-system = [", "explanation": "According to modern conventions" }',
                    '{ "before": "propagatedBuildInputs = [", "after": "dependencies = [", "explanation": "According to modern conventions" }',
                ],
            },
        },
    },
    "pkgs/development/python-modules/agent-client-protocol/default.nix": {
        "content": '1: {\n2:   lib,\n3:   buildPythonPackage,\n4:   fetchFromGitHub,\n5: \n6:   # build-system\n7:   pdm-backend,\n8: \n9:   # dependencies\n10:   pydantic,\n11: \n12:   # optional-dependencies\n13:   opentelemetry-sdk,\n14: \n15:   # tests\n16:   pytest-asyncio,\n17:   pytestCheckHook,\n18: }:\n19: \n20: buildPythonPackage rec {\n21:   pname = "agent-client-protocol";\n22:   version = "0.7.1";\n23:   pyproject = true;\n24: \n25:   src = fetchFromGitHub {\n26:     owner = "agentclientprotocol";\n27:     repo = "python-sdk";\n28:     tag = version;\n29:     hash = "sha256-pUOs6TUc0qmY+/AWTtm5kKouHKL8cLMhJ+nZT4r+6sI=";\n30:   };\n31: \n32:   build-system = [\n33:     pdm-backend\n34:   ];\n35: \n36:   dependencies = [\n37:     pydantic\n38:   ];\n39: \n40:   optional-dependencies = {\n41:     logfire = [\n42:       # logfire (unpackaged)\n43:       opentelemetry-sdk\n44:     ];\n45:   };\n46: \n47:   pythonImportsCheck = [ "acp" ];\n48: \n49:   nativeCheckInputs = [\n50:     pytest-asyncio\n51:     pytestCheckHook\n52:   ];\n53: \n54:   disabledTests = [\n55:     # Hangs forever\n56:     "test_spawn_agent_process_roundtrip"\n57:   ];\n58: \n59:   meta = {\n60:     description = "Python SDK for ACP clients and agents";\n61:     homepage = "https://github.com/agentclientprotocol/python-sdk";\n62:     changelog = "https://github.com/agentclientprotocol/python-sdk/releases/tag/${src.tag}";\n63:     license = lib.licenses.asl20;\n64:     maintainers = with lib.maintainers; [ GaetanLepage ];\n65:   };\n66: }',
        "review_points": {
            "finalAttrs": {
                "instructions": "Replace rec with finalAttrs in the builder function without breaking its recursiveness. finalAttrs is a more modern and efficient way to inherit attributes from stdenv in Nix.",
                "examples": [
                    '\n            {\n                "before": "buildPythonPackage rec {"\n                "after": "buildPythonPackage (finalAttrs {"\n                "explanation": "Replaces rec with finalAttrs in the builder function. Reminder to close the parentheses at the end of the builder function. This change allows for more efficient inheritance of attributes from stdenv in Nix, while maintaining the recursive nature of the builder function."\n            }\n            ',
                    '\n            {\n                "before": "tag = "v${version}";"\n                "after": "tag = "v${finalAttrs.version}";"\n                "explanation": "Keep the recursiveness of the builder function while replacing rec with finalAttrs. In this example, we replace version with finalAttrs.version to ensure that the builder function can still access the version attribute from stdenv without breaking its recursiveness."\n            }\n            ',
                    '\n            {\n                "before": "changelog = "https://github.com/holoviz/datashader/blob/${src.tag}/CHANGELOG.rst";"\n                "after": "changelog = "https://github.com/holoviz/datashader/blob/${finalAttrs.src.tag}/CHANGELOG.rst";"\n                "explanation": "Keep the builder function recursive by replacing rec with finalAttrs, which allows to inherit attributes from stdenv in a more modern and efficient way. In this example, we replace src.tag with finalAttrs.src.tag to maintain the recursive nature of the builder function while using finalAttrs for better performance and maintainability."\n            }\n            ',
                ],
            },
            "Modern Python build tools": {
                "instructions": "buildPythonPackage and buildPythonApplication have their own modern way to build a package. Using build-system instead of nativeBuildInputs and dependencies instead of propagatedBuildInputs is now the norm.",
                "examples": [
                    '{ "before": "nativeBuildInputs = [", "after": "build-system = [", "explanation": "According to modern conventions" }',
                    '{ "before": "propagatedBuildInputs = [", "after": "dependencies = [", "explanation": "According to modern conventions" }',
                ],
            },
        },
    },
    "pkgs/development/python-modules/textual-speedups/default.nix": {
        "content": '1: {\n2:   lib,\n3:   buildPythonPackage,\n4:   fetchFromGitHub,\n5:   rustPlatform,\n6: }:\n7: \n8: buildPythonPackage rec {\n9:   pname = "textual-speedups";\n10:   version = "0.2.1";\n11:   pyproject = true;\n12: \n13:   src = fetchFromGitHub {\n14:     owner = "willmcgugan";\n15:     repo = "textual-speedups";\n16:     tag = "v${version}";\n17:     hash = "sha256-zsDA8qPpeiOlmL18p4pItEgXQjgrQEBVRJazrGJT9Bw=";\n18:   };\n19: \n20:   cargoDeps = rustPlatform.fetchCargoVendor {\n21:     inherit pname version src;\n22:     hash = "sha256-Bz4ocEziOlOX4z5F9EDry99YofeGyxL/6OTIf/WEgK4=";\n23:   };\n24: \n25:   nativeBuildInputs = [\n26:     rustPlatform.cargoSetupHook\n27:     rustPlatform.maturinBuildHook\n28:   ];\n29: \n30:   pythonImportsCheck = [ "textual_speedups" ];\n31: \n32:   # No tests\n33:   doCheck = false;\n34: \n35:   meta = {\n36:     description = "Optional Rust speedups for Textual";\n37:     homepage = "https://github.com/willmcgugan/textual-speedups";\n38:     # No license (yet?)\n39:     # https://github.com/willmcgugan/textual-speedups/issues/2\n40:     license = lib.licenses.unfree;\n41:     maintainers = with lib.maintainers; [ GaetanLepage ];\n42:   };\n43: }',
        "review_points": {
            "finalAttrs": {
                "instructions": "Replace rec with finalAttrs in the builder function without breaking its recursiveness. finalAttrs is a more modern and efficient way to inherit attributes from stdenv in Nix.",
                "examples": [
                    '\n            {\n                "before": "buildPythonPackage rec {"\n                "after": "buildPythonPackage (finalAttrs {"\n                "explanation": "Replaces rec with finalAttrs in the builder function. Reminder to close the parentheses at the end of the builder function. This change allows for more efficient inheritance of attributes from stdenv in Nix, while maintaining the recursive nature of the builder function."\n            }\n            ',
                    '\n            {\n                "before": "tag = "v${version}";"\n                "after": "tag = "v${finalAttrs.version}";"\n                "explanation": "Keep the recursiveness of the builder function while replacing rec with finalAttrs. In this example, we replace version with finalAttrs.version to ensure that the builder function can still access the version attribute from stdenv without breaking its recursiveness."\n            }\n            ',
                    '\n            {\n                "before": "changelog = "https://github.com/holoviz/datashader/blob/${src.tag}/CHANGELOG.rst";"\n                "after": "changelog = "https://github.com/holoviz/datashader/blob/${finalAttrs.src.tag}/CHANGELOG.rst";"\n                "explanation": "Keep the builder function recursive by replacing rec with finalAttrs, which allows to inherit attributes from stdenv in a more modern and efficient way. In this example, we replace src.tag with finalAttrs.src.tag to maintain the recursive nature of the builder function while using finalAttrs for better performance and maintainability."\n            }\n            ',
                ],
            },
            "Modern Python build tools": {
                "instructions": "buildPythonPackage and buildPythonApplication have their own modern way to build a package. Using build-system instead of nativeBuildInputs and dependencies instead of propagatedBuildInputs is now the norm.",
                "examples": [
                    '{ "before": "nativeBuildInputs = [", "after": "build-system = [", "explanation": "According to modern conventions" }',
                    '{ "before": "propagatedBuildInputs = [", "after": "dependencies = [", "explanation": "According to modern conventions" }',
                ],
            },
        },
    },
}


def test_agent_service_rep_format_1():
    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")
    rep = agent_service.ask_agent_for_review(review_input=EXAMPLE_REVIEW_INPUT_1)
    assert type(rep) == dict
    assert type(rep["changes"]) == list
    assert type(rep["changes"][0]) == dict
    assert type(rep["changes"][0]["line_number"]) == int
    assert type(rep["changes"][0]["before"]) == str
    assert type(rep["changes"][0]["after"]) == str
    assert type(rep["changes"][0]["explanation"]) == str


def test_agent_service_rep_format_2():
    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")
    rep = agent_service.ask_agent_for_review(review_input=EXAMPLE_REVIEW_INPUT_2)
    assert type(rep) == dict
    assert type(rep["changes"]) == list
    assert type(rep["changes"][0]) == dict
    assert type(rep["changes"][0]["line_number"]) == int
    assert type(rep["changes"][0]["before"]) == str
    assert type(rep["changes"][0]["after"]) == str
    assert type(rep["changes"][0]["explanation"]) == str


def test_agent_service_initialization():
    """Test that AgentService initializes correctly."""
    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")
    assert agent_service.agent == AGENTS.MISTRAL
    assert agent_service.model == "devstral-latest"
    assert agent_service.system_prompt is not None
    assert len(agent_service.system_prompt) > 0


@patch("quality.review.services.agent.AGENTS.get_client_class")
def test_agent_service_missing_api_key(mock_get_client):
    """Test that AgentService handles missing API key."""
    mock_client_class = MagicMock()
    mock_get_client.return_value = mock_client_class

    # Mock the client to raise ValueError for missing API key
    mock_client_instance = MagicMock()
    mock_client_class.side_effect = ValueError("API key not found")

    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")

    with pytest.raises(ValueError, match="API key not found"):
        agent_service.ask_agent_for_review(review_input={"test": "data"})


@patch("quality.review.services.agent.AGENTS.get_client_class")
def test_agent_service_invalid_response_format(mock_get_client):
    """Test that AgentService handles invalid response format."""
    mock_client_class = MagicMock()
    mock_get_client.return_value = mock_client_class

    # Mock the client to return invalid response format
    mock_client_instance = MagicMock()
    mock_client_instance.ask.return_value = "invalid response format"
    mock_client_class.return_value = mock_client_instance

    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")

    with pytest.raises((ValueError, SyntaxError)):
        agent_service.ask_agent_for_review(review_input={"test": "data"})


@patch("quality.review.services.agent.AGENTS.get_client_class")
def test_agent_service_empty_response(mock_get_client):
    """Test that AgentService handles empty response."""
    mock_client_class = MagicMock()
    mock_get_client.return_value = mock_client_class

    # Mock the client to return empty response
    mock_client_instance = MagicMock()
    mock_client_instance.ask.return_value = ""
    mock_client_class.return_value = mock_client_instance

    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")

    with pytest.raises((ValueError, SyntaxError)):
        agent_service.ask_agent_for_review(review_input={"test": "data"})


@patch("quality.review.services.agent.AGENTS.get_client_class")
def test_agent_service_malformed_response(mock_get_client):
    """Test that AgentService handles malformed JSON response."""
    mock_client_class = MagicMock()
    mock_get_client.return_value = mock_client_class

    # Mock the client to return malformed JSON
    mock_client_instance = MagicMock()
    mock_client_instance.ask.return_value = '{"changes": ["malformed"}'
    mock_client_class.return_value = mock_client_instance

    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")

    with pytest.raises((ValueError, SyntaxError)):
        agent_service.ask_agent_for_review(review_input={"test": "data"})


@patch("quality.review.services.agent.AGENTS.get_client_class")
def test_agent_service_empty_changes_list(mock_get_client):
    """Test that AgentService handles empty changes list."""
    mock_client_class = MagicMock()
    mock_get_client.return_value = mock_client_class

    # Mock the client to return valid response with empty changes
    mock_client_instance = MagicMock()
    mock_client_instance.ask.return_value = '{"changes": []}'
    mock_client_class.return_value = mock_client_instance

    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")

    result = agent_service.ask_agent_for_review(review_input={"test": "data"})
    assert result == {"changes": []}


@patch("quality.review.services.agent.AGENTS.get_client_class")
def test_agent_service_missing_required_fields(mock_get_client):
    """Test that AgentService handles response with missing required fields."""
    mock_client_class = MagicMock()
    mock_get_client.return_value = mock_client_class

    # Mock the client to return response with missing fields
    mock_client_instance = MagicMock()
    mock_client_instance.ask.return_value = '{"changes": [{"line_number": 1}]}'
    mock_client_class.return_value = mock_client_instance

    agent_service = AgentService(agent=AGENTS.MISTRAL, model="devstral-latest")

    result = agent_service.ask_agent_for_review(review_input={"test": "data"})
    # Should still return the response even if fields are missing
    assert "changes" in result
    assert len(result["changes"]) == 1
    assert result["changes"][0]["line_number"] == 1
