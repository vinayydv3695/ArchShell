import os
import pytest
import subprocess
from command_hero.core import CommandHero


def test_echo(capsys):
    hero = CommandHero()
    hero._echo(["hello", "world"])
    captured = capsys.readouterr()
    assert "hello world" in captured.out


def test_pwd(capsys):
    hero = CommandHero()
    hero._pwd([])
    captured = capsys.readouterr()
    assert os.getcwd() in captured.out


def test_touch_and_cat(tmp_path, capsys):
    hero = CommandHero()
    test_file = tmp_path / "test.txt"
    
    # Touch file
    hero._touch([str(test_file)])
    assert test_file.exists()
    
    # Write content
    test_file.write_text("test content\n")
    
    # Cat file
    hero._cat([str(test_file)])
    captured = capsys.readouterr()
    assert "test content" in captured.out


def test_mkdir(tmp_path):
    hero = CommandHero()
    test_dir = tmp_path / "testdir"
    
    hero._mkdir([str(test_dir)])
    assert test_dir.exists()
    assert test_dir.is_dir()


def test_alias(capsys):
    hero = CommandHero()
    
    # Create alias
    hero._alias_cmd(["test=echo hello"])
    assert "test" in hero._aliases
    assert hero._aliases["test"] == "echo hello"
    
    # Expand alias
    expanded = hero._expand_alias("test world")
    assert expanded == "echo hello world"


def test_wc(tmp_path, capsys):
    hero = CommandHero()
    test_file = tmp_path / "test.txt"
    test_file.write_text("line1\nline2\nline3\n")
    
    hero._wc([str(test_file)])
    captured = capsys.readouterr()
    assert "3" in captured.out  # 3 lines


def test_grep(tmp_path, capsys):
    hero = CommandHero()
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello\nworld\nhello again\n")
    
    hero._grep(["hello", str(test_file)])
    captured = capsys.readouterr()
    assert "hello" in captured.out
    assert ":hello" in captured.out  # Contains the matched line


def test_edit_invokes_editor(monkeypatch):
    hero = CommandHero()

    called = {}

    def fake_call(cmd, *a, **kw):
        # record the command invoked and pretend it succeeded
        called['cmd'] = cmd
        return 0

    monkeypatch.setattr(subprocess, 'call', fake_call)

    # Call edit with a filename
    hero._edit(['/tmp/testfile.txt'])

    assert 'cmd' in called
    # Editor should be the first element and path should be last
    assert called['cmd'][-1] == '/tmp/testfile.txt'


def test_vim_and_nano_invokes(monkeypatch):
    hero = CommandHero()
    calls = []

    def fake_call(cmd, *a, **kw):
        calls.append(cmd)
        return 0

    monkeypatch.setattr(subprocess, 'call', fake_call)

    hero._vim(['/tmp/a'])
    hero._nano(['/tmp/b'])

    assert calls[0][0] == 'vim'
    assert calls[0][-1] == '/tmp/a'
    assert calls[1][0] == 'nano'
    assert calls[1][-1] == '/tmp/b'
