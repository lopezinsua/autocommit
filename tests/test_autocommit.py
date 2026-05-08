"""Tests for autocommit utilities."""
import pytest
from unittest.mock import MagicMock, patch

from autocommit import generate_message, get_staged_diff


def test_get_staged_diff_success():
    mock = MagicMock()
    mock.stdout = "diff --git a/f.py b/f.py\n+new line"
    mock.returncode = 0
    with patch("subprocess.run", return_value=mock):
        diff = get_staged_diff()
    assert "diff" in diff


def test_get_staged_diff_not_in_repo():
    mock = MagicMock()
    mock.stdout = ""
    mock.returncode = 128
    mock.stderr = "fatal: not a git repository"
    with patch("subprocess.run", return_value=mock):
        with pytest.raises(SystemExit):
            get_staged_diff()


def test_generate_message_en():
    mock_resp = MagicMock()
    mock_resp.choices[0].message.content = "feat(api): add search endpoint"
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_resp
    with patch("autocommit.Groq", return_value=mock_client):
        msg = generate_message("+ def search():", lang="en")
    assert msg == "feat(api): add search endpoint"


def test_generate_message_es():
    mock_resp = MagicMock()
    mock_resp.choices[0].message.content = "feat(api): agregar busqueda semantica"
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_resp
    with patch("autocommit.Groq", return_value=mock_client):
        msg = generate_message("+ def buscar():", lang="es")
    assert "agregar" in msg
