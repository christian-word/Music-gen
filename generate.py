import os
import google.generativeai as genai
import sys

# Получаем ключ из секретов GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Ошибка: API-ключ GEMINI_API_KEY не найден в секретах репозитория.")
    sys.exit(1)

# Настройка клиента
genai.configure(api_key=api_key)

async def generate_pro_track():
    print("🚀 Запускаем генерацию в Lyria 3 Pro...")
    
    # Промпт для Lyria Pro. Можно использовать теги структуры [Verse], [Chorus]
    # Напиши здесь свои стихи или просто подробное описание
    custom_prompt = """
    A cheerful acoustic folk pop song about travel and freedom. Upbeat tempo, acoustic guitar, harmonica, female vocals. 
    The tone should be warm and encouraging. Structure:
    [Verse 1]
    Pack your bags, the sun is high,
    Say goodbye to the everyday sky.
    The dusty road is calling my name,
    Nothing will ever be the same.
    [Chorus]
    Oh, the world is wide and free,
    A thousand places I want to see.
    With every mile my spirit grows,
    Where the river of freedom flows.
    """

    model = genai.GenerativeModel('lyria-3-pro-preview')
    
    # Генерация контента. Lyria Pro вернет структуру трека и само аудио
    response = await model.generate_content_async(
        contents=custom_prompt,
    )

    # Ищем бинарные данные аудио в ответе мультимодальной модели
    audio_found = False
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            audio_buffer = part.inline_data.data
            
            # Сохраняем файл на диск
            file_name = 'output_song.mp3'
            with open(file_name, 'wb') as f:
                f.write(audio_buffer)
            
            print(f"🎵 Успех! Песня сгенерирована и сохранена как {file_name}!")
            audio_found = True
            break
            
    if not audio_found:
        print("❌ Ошибка: Google вернул ответ, но в нем нет аудиоданных. Возможно, промпт заблокирован цензурой.")

# Запуск асинхронной функции
if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_pro_track())