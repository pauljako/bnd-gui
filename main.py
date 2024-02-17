#!/bin/python3
import threading
import customtkinter
import boundaries
import os


def run(name: str):
    thread = threading.Thread(target=boundaries.run, args=(name, []))
    thread.start()


def main():

    blacklist = ["bnd-gui"]

    app = customtkinter.CTk(className="bnd-gui")

    app.title("boundaries GUI")
    # app.geometry("400x150")
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    scrollable_frame = customtkinter.CTkScrollableFrame(app, label_text="Installed Apps")
    scrollable_frame.bind_all("<Button-4>", lambda e: scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
    scrollable_frame.bind_all("<Button-5>", lambda e: scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nesw")

    btn_row = 0
    buttons = []

    dir_content = os.listdir(boundaries.APP_DIR)
    for p in dir_content:
        info = boundaries.getpkginfo(p)
        if info is not None and "name" in info and "de_name" in info and not info["name"] in blacklist:
            btn_text = info["de_name"]

            buttons.append(customtkinter.CTkButton(scrollable_frame, text=btn_text, command=lambda x=info["name"]: run(x)))

            btn_row += 1

    for i in range(btn_row):
        buttons[i].grid(row=i, column=0, padx=20, pady=20, sticky="ew")

    app.mainloop()


if __name__ == '__main__':
    main()
