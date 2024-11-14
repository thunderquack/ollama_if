import gradio as gr
import ollama

# Инициализация глобальной истории сообщений
chat_history = []

# Получение списка доступных моделей из Ollama
def get_model_list():
    try:
        models_data = ollama.list()
        models = models_data.get('models', [])
        return [model['name'] for model in models]
    except Exception as e:
        print(f"Ошибка при получении списка моделей: {str(e)}")
        return []

# Функция для отправки промта с учетом истории сообщений
def generate_response(prompt, model_name):
    global chat_history  # Используем глобальную историю сообщений
    try:
        # Добавляем текущее сообщение пользователя в историю
        chat_history.append({'role': 'user', 'content': prompt})

        # Отправка запроса с историей сообщений к выбранной модели Ollama
        response = ollama.chat(
            model=model_name,
            messages=chat_history
        )

        # Извлечение ответа и добавление в историю
        reply = response['message']['content']
        chat_history.append({'role': 'assistant', 'content': reply})

        # Формируем HTML для отображения истории
        history_html = format_chat_history(chat_history)

        return reply, history_html
    except Exception as e:
        return f"Произошла ошибка: {str(e)}", ""

# Функция для очистки истории сообщений
def clear_history():
    global chat_history
    chat_history = []
    return "История очищена.", ""

# Форматирование истории чата с использованием HTML
def format_chat_history(history):
    formatted_history = ""
    for message in history:
        if message['role'] == 'user':
            formatted_history += f"<div style='color:blue;'><b>Пользователь:</b> {message['content']}</div><br>"
        else:
            formatted_history += f"<div style='color:green;'><b>Модель:</b> {message['content']}</div><br>"
    return formatted_history

# Загрузка списка моделей для выпадающего списка
model_options = get_model_list()

# Настройка интерфейса Gradio
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            model_dropdown = gr.Dropdown(choices=model_options, label="Выберите модель")
            prompt_input = gr.Textbox(lines=2, placeholder="Введите ваш промт здесь...")
            output_text = gr.Textbox(label="Ответ модели")
            
            # Кнопки для отправки промта и очистки истории
            submit_button = gr.Button("Отправить")
            clear_button = gr.Button("Очистить историю")
        
        with gr.Column(scale=2):
            history_output = gr.HTML(label="История чата")
        
        submit_button.click(fn=generate_response, inputs=[prompt_input, model_dropdown], outputs=[output_text, history_output])
        clear_button.click(fn=clear_history, inputs=[], outputs=[output_text, history_output])

# Запуск интерфейса
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
