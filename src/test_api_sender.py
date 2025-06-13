from api_sender import APISender

def main():
    sender = APISender()
    model_name="Llama 4 Scout"
    success_count = sender.generate_schedule(model_name)
    
    print(f"Успешно сгенерировано расписаний: {success_count}")
    return success_count > 0 

if __name__ == "__main__":
    main()