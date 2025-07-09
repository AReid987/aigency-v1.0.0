import aiohttp
from PIL import Image as PILImage

# from pocketbase import PocketBase
# from pocketbase.models.record import Record
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Image, RichLog


class LogScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back")
    ]
    def __init__(self, logs: list[dict], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logs = logs
        self.log_widget = RichLog()

    async def on_mount(self) -> None:
        for log in self.logs:
            self.log_widget.write(f"[{log.get('level', 'UNKNOWN')}] {log.get('message', 'No message')}")

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.log_widget
        yield Footer()

class GifScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back")
    ]
    def __init__(self, gif_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gif_path = gif_path
        self.gif_widget = Image.from_file(gif_path)

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.gif_widget
        yield Footer()

class TrajectoryScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back")
    ]
    def __init__(self, trajectories: list[dict], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trajectories = trajectories
        self.log_widget = RichLog()

    async def on_mount(self) -> None:
        for trajectory in self.trajectories:
            self.log_widget.write(str(trajectory.get('data', 'No data')))

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.log_widget
        yield Footer()

class ScreenshotScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back")
    ]

    def __init__(self, image_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_path = image_path
        self.image_widget = PILImage.from_file(image_path)

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.image_widget
        yield Footer()

class ProxyLiteApp(App):
    CSS_PATH = "tui.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("l", "view_logs", "View Logs"),
        Binding("g", "view_gifs", "View Gifs"),
        Binding("t", "view_trajectories", "View Trajectories"),
        Binding("s", "view_screenshots", "View Screenshots"),
    ]

    def __init__(self, pb_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pb_url = pb_url
        self.session = None # aiohttp session for managing connections
    
    async def on_mount(self) -> None:
        self.session = aiohttp.ClientSession()

    async def on_shutdown(self) -> None:
        if self.session:
            await self.session.close()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()


    async def load_logs(self):
        self.logs = []
        async with self.session.get(f"{self.pb_url}/api/collections/logs/records") as response:
            if response.status == 200:
                data = await response.json()
                self.logs = data.get("items")
            else:
                print(f"Error loading logs: {response.status}")

    async def load_trajectories(self):
        self.trajectories = []
        async with self.session.get(f"{self.pb_url}/api/collections/trajectories/records") as response:
            if response.status == 200:
                data = await response.json()
                self.trajectories = data.get("items")
            else:
                print(f"Error loading trajectories: {response.status}")

    async def action_view_logs(self) -> None:
        await self.load_logs()
        self.push_screen(LogScreen(self.logs))
    
    def action_view_gifs(self) -> None:
        self.push_screen(GifScreen("/packages/proxy-lite/gifs/demo.gif"))

    async def action_view_trajectories(self) -> None:
        await self.load_trajectories()
        self.push_screen(TrajectoryScreen(self.trajectories))


    def action_view_screenshots(self) -> None:
        self.push_screen(ScreenshotScreen("/packages/proxy-lite/screenshots/screenshot.png"))

async def run_tui(pb_url: str):
    app = ProxyLiteApp(pb_url)
    await app.run()