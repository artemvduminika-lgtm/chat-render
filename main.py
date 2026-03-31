import os
import asyncio
import websockets

# Множество подключенных клиентов
clients = set()

# Обработчик каждого WebSocket подключения
async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            # Отправляем сообщение всем остальным клиентам
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

# Главная функция запуска сервера
async def main():
    # Render передает порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting server on port {port}")
    
    # Запуск WebSocket сервера
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # держим сервер активным

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())
