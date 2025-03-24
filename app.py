import json
import threading
from tkinter import filedialog
import customtkinter as ctk
from agent_methods import CoverLetterAgent


with open("config/config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

cfg_main = config["Main"]
cfg_result = config["Response"]
cfg_tab = config["TabView"]
cfg_entry = config["EntryList"]
cfg_box = config["ToggleBox"]
cfg_edit = config["ToggleBoxButton"]
cfg_clr = config["Colours"]

data_files = [
    "Education & Awards",
    "Hobbies",
    "Projects",
    "Skills",
    "Work History"
]
packed_data = []
for f in data_files:
    with open(f"applicant data/{f}.json", "r", encoding="utf-8") as file:
        packed_data.append(json.load(file))

education_data, hobby_data, \
    project_data, skill_data, work_data = packed_data  # pylint: disable=W0632

agent = CoverLetterAgent()


class CoverGenWindow(ctk.CTk):
    """
    Main application window for the cover letter generator.
    """

    def __init__(self):
        """
        Initialize the CoverGenWindow, configure GUI components, and set
        layout.

        Sets window title, dimensions, creates tabs, input boxes, and buttons.
        """
        super().__init__()

        (
            self.win_result, self.window_text, self.save_button,
            self.copy_button, self.dot_animation
        ) = (None,) * 5

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
            command=self.generate_response,
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

    def generate_response(self):
        """
        Generate a cover letter response based on user input.

        Retrieves the job posting from the input box, initiates a loading
        animation, disables the button, and starts a thread to generate a
        response.
        """
        job_posting = self.input_box.get("1.0", "end").strip()

        self.animate_dots(0)
        self.gen_button.configure(state="disabled")

        threading.Thread(target=self._generate_response_thread,
                         args=(job_posting,)).start()

    def _generate_response_thread(self, job_posting):
        """
        Run the cover letter generation in a separate thread.

        Args:
            job_posting (str): The job posting description to use for
                               generating the cover letter.
        """
        response = agent.generate_cover_letter(job_posting)
        self.after(0, self.display_response, response)

    def animate_dots(self, step):
        """
        Animate a rotating line on the generate button while waiting for a
        response.

        Args:
            step (int): The current frame of the animation (0-3).
        """
        line_frames = ["|", "/", "—", "\\"]
        self.gen_button.configure(
            text=f" {line_frames[step]} Generating {line_frames[step]}")

        next_step = (step + 1) % 4
        self.dot_animation = self.after(100, self.animate_dots, next_step)

    def display_response(self, response):
        """
        Display the generated cover letter in a new window.

        Cancels the loading animation, resets the button, and opens a window
        displaying the response with options to save or copy.

        Args:
            response (str): The generated cover letter or an error message.
        """
        self.after_cancel(self.dot_animation)
        self.gen_button.configure(text="Generate Response", state="normal")

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

            self.window_text.insert("1.0", str(response))

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
            self.text_box.delete("1.0", "end")
            self.window_text.insert("1.0", str(response))
            self.win_result.lift()
            self.win_result.focus_force()

    def save_to_file(self):
        """
        Save the generated cover letter to a file.

        Opens a file dialog to select a save location and writes the text
        from the response window to a .txt file.
        """
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
        """
        Copy the generated cover letter to the system clipboard.

        Changes button text to indicate success and restores the original
        button text after a delay.
        """
        self.copy_button.configure(text="Copied")
        self.copy_button.after(
            2500, lambda: self.copy_button.configure(text="Copy to Clipboard")
        )
        self.clipboard_clear()
        self.clipboard_append(self.window_text.get("1.0", "end").strip())
        self.update()


class TabView(ctk.CTkTabview):
    """
    Tab view that organizes and manages multiple tabs for input data.
    """
    def __init__(self, master, **kwargs):
        """
        Initialize the TabView and add tabs for different types of applicant
        data.

        Args:
            master: Parent widget where the tab view will be placed.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
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
        """
        Disable binding to prevent unwanted interactions.
        """
        return

    def unbind(self, *args, **kwargs):
        """
        Disable unbinding to prevent unwanted interactions.
        """
        return


class Tab:
    """
    Tab for managing and editing applicant data with dynamic entry fields.
    """
    def __init__(self, master, dict_ref, box_num=0):
        """
        Initialize the Tab and create input fields and buttons.
        Always creates title box and upto 3 extra fields based on box_num.

        Args:
            master: Parent widget where the tab will be placed.
            dict_ref (dict): Dictionary reference containing applicant data.
            box_num (int): Number of additional editable boxes to display.
        """
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
        """
        Update tab details when a new entry is selected.

        Args:
            choice (str): The selected entry from the dropdown.
        """
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
        """
        Add a new entry to the data dictionary and update the dropdown.
        This also handles the different dict formats

        Opens a dialog to get the name of the new entry and updates the entry
        list.
        """
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
        """
        Update the dropdown values and optionally select a newly added entry.

        Args:
            new_entry (str, optional): The name of the newly added entry.
        """
        self.entry_list.configure(values=list(self.data.keys())[1:])
        if new_entry is not None:
            self.entry_list.set(new_entry)
            self.update_details(new_entry)

    def save_new_entries(self):
        """
        Save updated data entries to the corresponding JSON file.
        """
        tab_name = self.master_ref.master.get()
        with open(f"applicant data/{tab_name}.json", "w",
                  encoding="utf-8") as save_file:
            json.dump(self.data, save_file, ensure_ascii=False, indent=4)


class ToggleEditBox:
    """
    A text box with editable and non-editable states for modifying entries.
    """
    def __init__(self, master, combo_box_ref,
                 dict_ref, y_offset=0, title="", del_button=False):
        """
        Initialize the ToggleEditBox with editing capabilities and a button
        to switch between editing states.

        Optionally adds a delete button paired with the field.

        Args:
            master: Parent widget where the box is placed.
            combo_box_ref: Reference to the associated dropdown list.
            dict_ref (dict): Reference to the data dictionary.
            y_offset (int): Vertical offset for widget placement.
            title (str): Title label for the box.
            del_button (bool): Whether to add a delete button.
        """
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
        """
        Delete the selected entry after user confirmation.

        Prompts the user with a confirmation dialog and removes the selected
        entry from the data dictionary if confirmed.
        """
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
        """
        Toggle between editable and non-editable states.

        Saves changes made to the text box and updates the data dictionary
        when switching back to non-editable mode.

        Also handles the different formats of the various dictionaries.
        """
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
        """
        Update the contents of the text box.

        Args:
            text (str): New text to display in the text box.
        """
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", str(text or "Click Edit to type"))
        self.text_box.configure(state="disabled")

    def save_edit(self):
        """
        Save edits to the corresponding JSON file after changes are made.
        """
        tab_name = self.master_ref.master.get()
        with open(f"applicant data/{tab_name}.json", "w",
                  encoding="utf-8") as save_loc:
            json.dump(self.dict_ref, save_loc, ensure_ascii=False, indent=4)
