import json
from tkinter import filedialog
import customtkinter as ctk

with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

cfg_main = config["Main"]
cfg_result = config["Response"]
cfg_tab = config["TabView"]
cfg_entry = config["EntryList"]
cfg_box = config["ToggleBox"]
cfg_edit = config["ToggleBoxButton"]
cfg_clr = config["Colours"]

data_files = [
    "Education & Awards.json",
    "Hobbies.json",
    "Projects.json",
    "Skills.json",
    "Work History.json"
]
packed_data = []
for f in data_files:
    with open(f"applicant data./{f}", "r", encoding="utf-8") as file:
        packed_data.append(json.load(file))

education_data, hobby_data, \
    project_data, skill_data, work_data = packed_data  # pylint: disable=W0632


class CoverGenWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        (
            self.win_result, self.window_text, self.save_button,
            self.copy_button
        ) = (None,) * 4

        self.title(cfg_main["title"])
        self.geometry(f"{cfg_main["size_x"]}x{cfg_main["size_y"]}")
        self.resizable(False, False)

        self.tab_view = TabView(
            master=self,
            width=cfg_tab["size_x"],
            height=cfg_tab["size_y"]
        )
        self.input_box = ctk.CTkTextbox(
            master=self,
            width=cfg_tab["size_x"],
            height=cfg_main["size_y"]-cfg_tab["size_y"]*1.2,
            border_color=cfg_clr["blue"],
            wrap="word",
            border_width=2,
            border_spacing=1
        )
        self.gen_button = ctk.CTkButton(
            master=self,
            width=cfg_tab["size_x"],
            text="Generate Response",
            command=self.display_response,
            fg_color=cfg_clr["blue"],
            border_color=cfg_clr["dark_blue"],
            border_width=2,
            border_spacing=1
        )

        self.gen_button.place(
            x=cfg_tab["pos_x"],
            y=1.6*cfg_tab["pos_x"]+cfg_main["size_y"]-cfg_tab["size_y"]*1.2,
        )
        self.tab_view.place(x=cfg_tab["pos_x"], y=cfg_tab["pos_y"])
        self.input_box.place(x=cfg_tab["pos_x"], y=cfg_tab["pos_x"])

    def display_response(self):
        # TODO: link response to agent response + setup agent
        response = """Dear [Hiring Manager's Name],

I am writing to express my interest in the [Job Title] position at [Company
 Name]. With a Master's degree in Artificial Intelligence and hands-on
 experience in machine learning, data science, and software development,
 I am confident in my ability to contribute effectively to your team

 During my time at the University of Surrey, I worked on various projects
 including

 Developing a 3D object detection system for LiDAR point clouds as part o
 my Master's thesis
 Implementing NLP models for sentiment analysis and market predictions
 Designing AI-driven systems, such as a custom cover letter generator and
 AI-powered CV enhancement tools
 I am highly motivated to apply my technical expertise and problem-solving
 abilities to [Company Name], where I can further develop my skills whil
 contributing to impactful projects. I am particularly drawn to your
 organization because of [mention something specific about the compan
 or its projects that interests you]

 I am eager to discuss how my background aligns with the requirements of
 this position. Thank you for your time and consideration. I look forward
 to the possibility of contributing to your team.

Best regards,
[Your Name]"""

        # TODO: Visualise waiting on generate button for the response.

        if self.win_result is None or not self.win_result.winfo_exists():
            self.win_result = ctk.CTkToplevel(self)

            self.win_result.geometry(
                f"{cfg_main["size_x"]}x{cfg_main["size_y"]}")
            self.win_result.title("Cover Letter Response")
            self.win_result.attributes('-topmost', True)
            self.win_result.resizable(False, False)

            self.window_text = ctk.CTkTextbox(
                master=self.win_result,
                width=cfg_result["size_x"],
                height=cfg_result["size_y"],
                wrap="word"
            )
            self.save_button = ctk.CTkButton(
                master=self.win_result,
                width=cfg_entry["size_x"] * 0.5,
                height=cfg_entry["size_y"],
                command=self.save_to_file,
                text="Save text file"
            )
            self.copy_button = ctk.CTkButton(
                master=self.win_result,
                width=cfg_entry["size_x"] * 0.5,
                height=cfg_entry["size_y"],
                command=self.copy_to_clipboard,
                text="Copy to Clipboard"
            )

            self.window_text.insert("1.0", response)

            self.save_button.place(x=cfg_result["pos_x"],
                                   y=cfg_result["pos_y"])
            self.window_text.place(x=cfg_result["pos_x"],
                                   y=cfg_result["pos_x"])
            self.copy_button.place(
                x=cfg_result["pos_x"]+cfg_result["size_x"] -
                cfg_entry["size_x"]*0.5,
                y=cfg_result["pos_y"]
            )
        else:
            self.win_result.lift()
            self.win_result.focus_force()

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(
            parent=self.win_result,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save File"
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as save_file:
                save_file.write(self.window_text.get("1.0", "end").strip())

    def copy_to_clipboard(self):
        self.copy_button.configure(text="Copied")
        self.copy_button.after(
            2500, lambda: self.copy_button.configure(text="Copy to Clipboard")
        )
        self.clipboard_clear()
        self.clipboard_append(self.window_text.get("1.0", "end").strip())
        self.update()


class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Skills")
        self.add("Education & Awards")
        self.add("Work History")
        self.add("Projects")
        self.add("Hobbies")

        self.skill_tab = Tab(
            master=self.tab("Skills"),
            dict_ref=skill_data
        )
        self.job_tab = Tab(
            master=self.tab("Education & Awards"),
            dict_ref=education_data,
            box_num=2
        )
        self.skill_tab = Tab(
            master=self.tab("Work History"),
            dict_ref=work_data,
            box_num=3
        )
        self.job_tab = Tab(
            master=self.tab("Projects"),
            dict_ref=project_data,
            box_num=3
        )
        self.skill_tab = Tab(
            master=self.tab("Hobbies"),
            dict_ref=hobby_data
        )

    def bind(self, *args, **kwargs):
        # blank overwrite
        pass

    def unbind(self, *args, **kwargs):
        # blank overwrite
        pass


class Tab:
    def __init__(self, master, dict_ref, box_num=0):
        self.master_ref = master
        self.data = dict_ref
        self.desc_boxes = []

        self.entry_list = ctk.CTkComboBox(
            master=master,
            width=cfg_entry["size_x"],
            height=cfg_entry["size_y"],
            values=list(dict_ref.keys())[1:],
            command=self.update_details,
            state="readonly"
        )
        self.add_entry = ctk.CTkButton(
            master=master,
            width=cfg_entry["size_x"] * 0.5,
            height=cfg_entry["size_y"],
            text="Add Entry",
            command=self.add_new_entry,
            fg_color=cfg_clr["blue"],
            border_color=cfg_clr["dark_blue"],
            border_width=2,
            border_spacing=1
        )
        for i in range(box_num + 1):
            self.desc_boxes.append(
                ToggleEditBox(
                    master=master,
                    combo_box_ref=self.entry_list,
                    dict_ref=dict_ref,
                    y_offset=(cfg_box["size_y"] + 120)*0.25*min(i, 1)
                    + max(0, i - 1) * (cfg_box["size_y"] + 30),
                    title="" if i == 0 else list(
                        dict_ref["__Formatting"].keys())[i - 1],
                    del_button=(i == 0)
                )
            )

        self.entry_list.set(next(iter(list(dict_ref.keys())[1:]), ""))

        self.entry_list.place(x=cfg_entry["pos_x"], y=cfg_entry["pos_y"])
        self.add_entry.place(
            x=cfg_entry["pos_x"] + cfg_entry["size_x"] + 21,
            y=cfg_entry["pos_y"]
        )

        if len(list(self.data)) > 1:
            self.update_details(list(self.data.keys())[1])

    def update_details(self, choice):
        choice_data = []
        self.desc_boxes[0].update_box(text=choice)
        if self.data["__Formatting"] is not None:
            for value in self.data[choice].values():
                choice_data.append(value)
        for box, data in zip(self.desc_boxes[1:], choice_data):
            box.edit_button.configure(text="Edit")
            box.is_editing = False
            box.update_box(text=data)

    def add_new_entry(self):
        new_entry_dialog = ctk.CTkInputDialog(text=" ", title="Add New Entry")
        new_entry = new_entry_dialog.get_input()

        if new_entry and new_entry.strip():
            if self.data["__Formatting"] is None:
                self.data[new_entry] = None
            else:
                self.data[new_entry] = self.data["__Formatting"].copy()
            self.save_new_entries()
            self.update_entry_list(new_entry=new_entry)

    def update_entry_list(self, new_entry=None):
        self.entry_list.configure(values=list(self.data.keys())[1:])
        if new_entry is not None:
            self.entry_list.set(new_entry)
            self.update_details(new_entry)

    def save_new_entries(self):
        tab_name = self.master_ref.master.get()
        with open(f"applicant data/{tab_name}.json", "w",
                  encoding="utf-8") as save_file:
            json.dump(self.data, save_file, ensure_ascii=False, indent=4)


class ToggleEditBox:
    def __init__(self, master, combo_box_ref,
                 dict_ref, y_offset=0, title="", del_button=False):
        self.master_ref = master
        self.combo_box_ref = combo_box_ref
        self.dict_ref = dict_ref
        self.title = title
        self.is_editing = False

        self.label = ctk.CTkLabel(master=master, text=self.title)
        self.text_box = ctk.CTkTextbox(
            master=master,
            width=cfg_box["size_x"],
            height=cfg_box["size_y"]*0.25 if del_button else cfg_box["size_y"],
            wrap="word",
            border_color=cfg_clr["black"],
            border_width=2,
            border_spacing=1
        )
        self.edit_button = ctk.CTkButton(
            master=master,
            width=cfg_edit["size_x"],
            height=cfg_entry["size_y"],
            text="Edit",
            command=self.toggle_edit,
            fg_color=cfg_clr["blue"],
            border_color=cfg_clr["dark_blue"],
            border_width=2,
            border_spacing=1
        )
        if del_button:
            self.delete_button = ctk.CTkButton(
                master=master,
                width=cfg_edit["size_x"],
                height=cfg_entry["size_y"],
                text="Delete Entry",
                command=self.delete_entry,
                fg_color=cfg_clr["red"],
                border_color=cfg_clr["dark_red"],
                border_width=2,
                border_spacing=1
            )
            self.delete_button.place(x=cfg_box["pos_x"],
                                     y=cfg_box["pos_y"] + y_offset)

        self.label.place(x=cfg_box["pos_x"], y=cfg_box["pos_y"] + y_offset)
        self.edit_button.place(x=cfg_edit["pos_x"],
                               y=cfg_box["pos_y"] + y_offset)
        self.text_box.place(x=cfg_box["pos_x"],
                            y=cfg_box["pos_y"] + 25 + y_offset)

        self.text_box.configure(state="disabled")

    def delete_entry(self):
        confirmation = ctk.CTkInputDialog(
            text="Type 'Yes' to confirm deletion",
            title="Delete Entry?"
        )
        response = confirmation.get_input()
        if response == "Yes":
            self.dict_ref.pop(self.combo_box_ref.get(), None)
            self.combo_box_ref.configure(values=list(self.dict_ref.keys())[1:])
            self.combo_box_ref.set(value="")
            self.update_box(text="Select or create a new entry.")

    def toggle_edit(self):
        """Toggles between editing and saving job details."""
        if self.is_editing:
            selected = self.combo_box_ref.get()
            if selected in self.dict_ref:
                new_text = self.text_box.get("1.0", "end").strip()
                if self.title == "":
                    if new_text in self.dict_ref and new_text != selected:
                        self.update_box(selected)
                        self.text_box.after(
                            20, lambda: self.text_box.configure(
                                border_color=cfg_clr["red"])
                        )
                        self.text_box.after(
                            1000, lambda: self.text_box.configure(
                                border_color=cfg_clr["black"])
                        )
                    else:
                        value = self.dict_ref.pop(selected, None)
                        self.dict_ref[new_text] = value
                        self.combo_box_ref.configure(
                            values=list(self.dict_ref.keys())[1:])
                        self.combo_box_ref.set(new_text)
                elif new_text == "Click Edit to type":
                    self.dict_ref[selected][self.title] = None
                else:
                    self.dict_ref[selected][self.title] = new_text
                self.save_edit()
            self.text_box.configure(state="disabled",
                                    border_color=cfg_clr["black"])
            self.edit_button.configure(text="Edit")
        else:
            self.text_box.configure(state="normal",
                                    border_color=cfg_clr["green"])
            self.edit_button.configure(text="Save")

        self.is_editing = not self.is_editing

    def update_box(self, text=" "):
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", str(text or "Click Edit to type"))
        self.text_box.configure(state="disabled")

    def save_edit(self):
        tab_name = self.master_ref.master.get()
        with open(f"applicant data/{tab_name}.json", "w",
                  encoding="utf-8") as save_loc:
            json.dump(self.dict_ref, save_loc, ensure_ascii=False, indent=4)
