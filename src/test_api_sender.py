from api_sender import APISender

def main():
    sender = APISender()
    model_name = "DeepSeek R1" 
    try:
        response = sender.send_message(model_name = model_name)
        print("Ответ:\n", response)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
