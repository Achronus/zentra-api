import pytest
from pydantic import ValidationError
from zentra_api.validation import EnvFilename, SingleWord


class TestEnvFilename:
    @staticmethod
    def test_valid_filename():
        valid_filenames = [
            ".env",
            ".env.local",
            ".env.production",
            ".env.test",
            ".env.custom-1",
        ]

        for filename in valid_filenames:
            env_filename = EnvFilename(name=filename)
            assert env_filename.name == filename

    @staticmethod
    def test_invalid_filename():
        invalid_filenames = [
            "env",
            ".env.",
            ".env..local",
            ".env/production",
            ".env@custom",
        ]

        for filename in invalid_filenames:
            with pytest.raises(ValidationError):
                EnvFilename(name=filename)


class TestSingleWord:
    @staticmethod
    def test_valid_word():
        valid_words = ["hello", "world", "foo", "bar"]

        for word in valid_words:
            single_word = SingleWord(value=word)
            assert single_word.value == word

    @staticmethod
    def test_invalid_word():
        invalid_words = ["hello world", "foo bar", "foo-bar", "foo_bar"]

        for word in invalid_words:
            with pytest.raises(ValidationError):
                SingleWord(value=word)
