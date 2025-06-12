from api_sender import APISender

def main():
    sender = APISender()
    model_name = "DeepSeek R1"  # Здесь можно указать нужную модель, например: "Llama", "Qwen3-235B-A22B" и т.д.
    try:
        # Просто отправляем тестовый запрос, всё остальное внутри APISender
        response = sender.send_message(model_name = model_name)
        print("Ответ:\n", response)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
