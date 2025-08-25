from langchain_ollama import ChatOllama


def implement_model(model_name):
    return ChatOllama(
        model=model_name, temperature=0.7, base_url="http://localhost:11434"
    )


def implement_stream_query_model(model, prompt):
    response_stream = model.stream([{"role": "user", "content": prompt}])
    content = ""
    for chunk in response_stream:
        print(chunk.content, end="", flush=True)
        content += chunk.content
    print()
    return content


def implement_compare_models_streaming(test_prompt):
    gemma3 = implement_model("gemma3:1b")
    phi3 = implement_model("phi3:mini")
    print("🌐Streaming gemma3:1b response:")
    response_gemma3 = implement_stream_query_model(gemma3, test_prompt)
    print()
    print("🌐Streaming phi3:mini response:")
    response_phi3 = implement_stream_query_model(phi3, test_prompt)
    print()
    return {"gemma3:1b": response_gemma3, "phi3:mini": response_phi3}


def main():
    print("🚀 Ollama Model Exercise (LangChain Integration)")
    print("=" * 55)
    print()

    try:
        test_prompt = input("Enter your prompt: ")

        print("🔄 Testing your model comparison:")
        print()

        print("🌐Comparison results:")
        comparison = implement_compare_models_streaming(test_prompt)

        print("\n🎉 All implementations working!")
        print("✅ Great job implementing the LangChain-Ollama patterns!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
