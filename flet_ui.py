import flet as ft
from audio_loop import AudioLoop
import asyncio

def main(page: ft.Page):
    page.title = "AI Assistant"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 20

    # Variabel untuk menyimpan status aplikasi
    is_running = False
    audio_loop = None

    # Widget untuk menampilkan log
    log = ft.Text("Log akan muncul di sini...", size=16, color="white")

    async def start_audio_loop(e):
        nonlocal is_running, audio_loop
        if not is_running:
            is_running = True
            log.value = "AI Assistant dimulai..."
            start_button.text = "Stop AI Assistant"
            page.update()

            audio_loop = AudioLoop()
            await audio_loop.run()

            is_running = False
            log.value = "AI Assistant dihentikan."
            start_button.text = "Start AI Assistant"
            page.update()

    start_button = ft.ElevatedButton("Start AI Assistant", on_click=start_audio_loop)

    page.add(
        ft.Column(
            [
                ft.Text("AI Assistant", size=30, weight="bold"),
                ft.Container(
                    content=log,
                    padding=10,
                    bgcolor="blue",
                    border_radius=10,
                ),
                start_button,
            ],
            spacing=20,
        )
    )

ft.app(target=main)