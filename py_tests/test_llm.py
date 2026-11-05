"""Testing the LLM if can respond"""



#test the LLM respons
def test_get_llm_returns_response_text(mock_manager):
    mock_manager.client.models.generate_content.return_value.text = "ok"

    result = mock_manager.get_llm("Ok")

    assert result == "ok"
    #validate that the method has been called once
    mock_manager.client.models.generate_content.assert_called_once()

    kwargs = mock_manager.models.generate_content.call_args.kwargs
    assert kwargs["model"] == "test-model"
    assert kwargs["contents"] == "Ok"
    assert kwargs["config"].temperature == 0.2