import pytest
from unittest.mock import patch, MagicMock
from services.ai_moderation import is_text_toxic, generate_reply


@pytest.mark.asyncio
class TestAIModeration:
    @patch("services.ai_moderation.client.models.generate_content")
    def test_is_text_toxic_manual_detection(self, mock_generate_content):
        # Тест перевіряє ручну перевірку чорного списку
        toxic_text = "Це хуйня, а не текст."
        result = is_text_toxic(toxic_text)
        assert result is True

    @patch("services.ai_moderation.client.models.generate_content")
    def test_is_text_toxic_ai_detection_yes(self, mock_generate_content):
        # Мокаємо відповідь від AI як "YES"
        mock_response = MagicMock()
        mock_response.text = "YES"
        mock_generate_content.return_value = mock_response

        non_toxic_text = "Цей текст потенційно токсичний."
        result = is_text_toxic(non_toxic_text)

        mock_generate_content.assert_called_once()
        assert result is True

    @patch("services.ai_moderation.client.models.generate_content")
    def test_is_text_toxic_ai_detection_no(self, mock_generate_content):
        # Мокаємо відповідь від AI як "NO"
        mock_response = MagicMock()
        mock_response.text = "NO"
        mock_generate_content.return_value = mock_response

        non_toxic_text = "Звичайний текст без образ."
        result = is_text_toxic(non_toxic_text)

        mock_generate_content.assert_called_once()
        assert result is False

    @patch("services.ai_moderation.client.models.generate_content")
    def test_is_text_toxic_ai_error(self, mock_generate_content):
        # Симулюємо помилку при виклику AI
        mock_generate_content.side_effect = Exception("AI error")

        text = "Текст для перевірки."
        result = is_text_toxic(text)

        mock_generate_content.assert_called_once()
        assert result is False

    @patch("services.ai_moderation.client.models.generate_content")
    def test_generate_reply_success(self, mock_generate_content):
        # Мокаємо успішну відповідь від AI
        mock_response = MagicMock()
        mock_response.text = "Дякую за ваш коментар!"
        mock_generate_content.return_value = mock_response

        post_text = "Ось мій пост."
        comment_text = "Це цікавий коментар."

        reply = generate_reply(post_text, comment_text)

        mock_generate_content.assert_called_once()
        assert reply == "Дякую за ваш коментар!"

    @patch("services.ai_moderation.client.models.generate_content")
    def test_generate_reply_error(self, mock_generate_content):
        # Симулюємо помилку при виклику AI
        mock_generate_content.side_effect = Exception("AI error")

        post_text = "Ось мій пост."
        comment_text = "Це цікавий коментар."

        reply = generate_reply(post_text, comment_text)

        mock_generate_content.assert_called_once()
        assert reply == "Дякую за ваш коментар!"