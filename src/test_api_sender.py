from api_sender import APISender

def main():
    sender = APISender()
    #                0              1               2              3              4               5              6                  7               8               9                       10   
    model_name = ["Kimi Dev", "Qwen3-235B-A22B", "Qwen2.5-72B", "DeepSeek V3", "DeepSeek R1", "DeepSeek R1T", "Gemini 2 Pro", "Llama 4 Scout",  "MAI DS R1", "NVIDIA: Llama 3.3", "Deepseek R1 Qwen3 8B"][0]
    success_count = sender.generate_schedule(model_name)
    
    print(f"Успешно сгенерировано расписаний: {success_count}")
    return success_count > 0 

if __name__ == "__main__":
    main()