"""Public Gradio showcase entry point."""
import os

from showcase import build_app


if __name__ == "__main__":
    build_app().launch(server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
                       server_port=int(os.getenv("PORT", "7860")), share=False,
                       max_file_size="1mb")
