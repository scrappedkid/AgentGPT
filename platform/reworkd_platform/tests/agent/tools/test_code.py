import pytest
from unittest.mock import patch, MagicMock
from reworkd_platform.web.api.agent.tools.code import Code

def test_call():
    with patch.object(Code, 'generate_code_stream', return_value=b'code'), \
         patch.object(Code, 'parse_code_from_stream', return_value='parsed code'), \
         patch.object(Code, 'write_to_shared_folder'), \
         patch.object(Code, 'generate_tags', return_value=[]):
        code = Code()
        response = code.call('goal', 'task', 'input')
        assert response.status_code == 200
        assert response.body == b'code'

def test_generate_code_stream():
    with patch('langchain.LLMChain.generate_text', return_value='code'):
        code = Code()
        result = code.generate_code_stream(MagicMock())
        assert result == b'code'

def test_parse_code_from_stream():
    code = Code()
    result = code.parse_code_from_stream(b'```python\ncode\n```')
    assert result == 'code'

def test_write_to_shared_folder(tmp_path):
    code = Code()
    file_path = tmp_path / "test.txt"
    code.write_to_shared_folder(str(file_path), 'content')
    assert file_path.read_text() == 'content'

def test_generate_tags():
    code = Code()
    result = code.generate_tags('code')
    assert result == []
