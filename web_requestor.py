import gradio as gr
import ollama
import json

# Получение списка доступных моделей из Ollama
def get_model_list():
    try:
        # Получаем строку JSON и преобразуем в словарь
        models = json.loads(ollama.list())
        return [model['name'] for model in models]
    except Exception as e:
        print(f"Ошибка при получении списка моделей: {str(e)}")
        return []

# Функция для отправки промта с выбранной моделью
def generate_response(prompt, model_name):
    try:
        # Отправка запроса к выбранной модели Ollama
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

# Загрузка списка моделей для выпадающего списка
model_options = get_model_list()

# Настройка интерфейса Gradio
iface = gr.Interface(
    fn=generate_response,
    inputs=[
        gr.Dropdown(choices=model_options, label="Выберите модель"),
        gr.Textbox(lines=2, placeholder="Введите ваш промт здесь...")
    ],
    outputs="text",
    title="Ollama Web Interface",
    description="Веб-интерфейс для взаимодействия с моделью Ollama через API"
)

# Запуск интерфейса
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
