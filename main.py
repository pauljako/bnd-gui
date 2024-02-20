#!/bin/python3
import threading
import customtkinter
import boundaries
import os


def install():

    filetypes = (
        ('All files', '*.*'),
    )

    file = customtkinter.filedialog.askopenfile(initialdir="~", filetypes=filetypes, title="Select File to Install")

    install_win = customtkinter.CTk(className="bnd-gui")
    install_win.title("Installing")
    install_win.grid_columnconfigure(0, weight=1)
    install_win.grid_rowconfigure(0, weight=1)

    progress_bar = customtkinter.CTkProgressBar(install_win, mode="indeterminate")
    progress_bar.grid(row=0, column=0, padx=20, pady=20, sticky="new")
    progress_bar.start()

    install_win.mainloop()


def run(name: str):
    thread = threading.Thread(target=boundaries.run, args=(name, []))
    thread.start()


def details_win(name: str):

    info = boundaries.getpkginfo(name)

    if info is None or "name" not in info:
        print("Not Found")
        return False

    if "de_name" in info:
        title = info["de_name"]
    else:
        title = info["name"]

    detail_win = customtkinter.CTk(className="bnd-gui")

    detail_win.title(title)
    detail_win.grid_columnconfigure(0, weight=1)
    detail_win.grid_rowconfigure(0, weight=1)

    top_frame = customtkinter.CTkFrame(detail_win)
    top_frame.grid_columnconfigure(0, weight=3)
    top_frame.grid_columnconfigure(1, weight=1)
    top_frame.grid_rowconfigure(0, weight=1)
    top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="new")

    title_label = customtkinter.CTkLabel(top_frame, text=title)
    title_label.grid(row=0, column=0, padx=20, pady=20, sticky="nesw")

    launch_button = customtkinter.CTkButton(top_frame, text="Launch", command=lambda x=info["name"]: run(x))
    launch_button.grid(row=0, column=1, padx=20, pady=20, sticky="nesw")

    detail_win.mainloop()


def main():

    blacklist = ["bnd-gui"]

    app = customtkinter.CTk(className="bnd-gui")

    app.title("boundaries GUI")
    app.geometry("400x550")
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)

    add_button = customtkinter.CTkButton(app, text="Install", command=install)
    add_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

    scrollable_frame = customtkinter.CTkScrollableFrame(app, label_text="Installed Apps")
    scrollable_frame.bind_all("<Button-4>", lambda e: scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
    scrollable_frame.bind_all("<Button-5>", lambda e: scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nesw")

    btn_row = 0
    buttons = []

    dir_content = os.listdir(boundaries.APP_DIR)
    for p in dir_content:
        info = boundaries.getpkginfo(p)
        if info is not None and "name" in info and "de_name" in info and not info["name"] in blacklist:
            btn_text = info["de_name"]

            buttons.append(customtkinter.CTkButton(scrollable_frame, text=btn_text, command=lambda x=info["name"]: details_win(x)))

            btn_row += 1

    for i in range(btn_row):
        buttons[i].grid(row=i, column=0, padx=20, pady=20, sticky="ew")

    app.mainloop()


if __name__ == '__main__':
    main()
