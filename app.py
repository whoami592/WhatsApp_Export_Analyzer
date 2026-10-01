import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from parser import parse_export, statistics


BG, PANEL, GREEN, DIM, TEXT = "#020805", "#07130d", "#00ff66", "#0a6b35", "#b7ffd0"


class WhatsAppExportAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WhatsApp Export Analyzer — Mr Sabaz Ali Khan")
        self.root.geometry("1120x720")
        self.root.minsize(850, 560)
        self.root.configure(bg=BG)
        self.messages = []
        self.filtered = []
        self._style()
        self._ui()

    def _style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=TEXT,
                        rowheight=27, borderwidth=0, font=("Consolas", 10))
        style.configure("Treeview.Heading", background=DIM, foreground="white", font=("Consolas", 10, "bold"))
        style.map("Treeview", background=[("selected", "#145a32")])

    def _ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=18, pady=(15, 8))
        tk.Label(header, text="WHATSAPP EXPORT ANALYZER", bg=BG, fg=GREEN,
                 font=("Consolas", 22, "bold")).pack(side="left")
        tk.Label(header, text="AUTHORIZED • OFFLINE • PRIVACY-FIRST", bg=BG, fg="#62ff9b",
                 font=("Consolas", 10)).pack(side="right")

        controls = tk.Frame(self.root, bg=PANEL, highlightbackground=DIM, highlightthickness=1)
        controls.pack(fill="x", padx=18, pady=7)
        self._button(controls, "IMPORT EXPORTED .TXT", self.open_file).pack(side="left", padx=8, pady=10)
        self._button(controls, "EXPORT RESULTS .CSV", self.export_csv).pack(side="left", padx=4)
        tk.Label(controls, text="SEARCH:", bg=PANEL, fg=GREEN, font=("Consolas", 10, "bold")).pack(side="left", padx=(25, 5))
        self.query = tk.StringVar()
        entry = tk.Entry(controls, textvariable=self.query, bg="#010503", fg=TEXT, insertbackground=GREEN,
                         relief="flat", font=("Consolas", 11), width=30)
        entry.pack(side="left", ipady=6)
        self.query.trace_add("write", lambda *_: self.apply_filter())

        self.status = tk.StringVar(value="READY — Import a WhatsApp exported chat text file")
        tk.Label(self.root, textvariable=self.status, bg=BG, fg="#73ffab", anchor="w",
                 font=("Consolas", 10)).pack(fill="x", padx=20, pady=4)

        body = tk.PanedWindow(self.root, orient="horizontal", bg=BG, sashwidth=5)
        body.pack(fill="both", expand=True, padx=18, pady=5)
        table_frame = tk.Frame(body, bg=PANEL)
        stats_frame = tk.Frame(body, bg=PANEL, width=270, highlightbackground=DIM, highlightthickness=1)
        body.add(table_frame, stretch="always")
        body.add(stats_frame, minsize=230)

        self.tree = ttk.Treeview(table_frame, columns=("date", "time", "sender", "message"), show="headings")
        for col, width in (("date", 100), ("time", 90), ("sender", 150), ("message", 510)):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=width, minwidth=70, stretch=col == "message")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tk.Label(stats_frame, text="ANALYSIS", bg=PANEL, fg=GREEN, font=("Consolas", 15, "bold")).pack(pady=(16, 7))
        self.stats_text = tk.Text(stats_frame, bg=PANEL, fg=TEXT, insertbackground=GREEN, relief="flat",
                                  font=("Consolas", 10), wrap="word", state="disabled")
        self.stats_text.pack(fill="both", expand=True, padx=14, pady=5)
        tk.Label(self.root, text="Coded by Cyber Security Engineer Mr Sabaz Ali Khan",
                 bg=BG, fg=DIM, font=("Consolas", 9)).pack(pady=(2, 9))

    def _button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, bg="#063d20", fg="white",
                         activebackground=GREEN, activeforeground="black", relief="flat",
                         font=("Consolas", 10, "bold"), padx=12, pady=7, cursor="hand2")

    def open_file(self):
        path = filedialog.askopenfilename(title="Select your exported WhatsApp chat", filetypes=[("Text files", "*.txt")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8-sig", errors="replace") as handle:
                self.messages = parse_export(handle.read())
            self.apply_filter()
            self.status.set(f"LOADED {len(self.messages)} MESSAGES — Data stays on this computer")
            if not self.messages:
                messagebox.showwarning("No messages found", "The file format was not recognized. Export the chat without media and try again.")
        except OSError as exc:
            messagebox.showerror("Import failed", str(exc))

    def apply_filter(self):
        term = self.query.get().strip().lower()
        self.filtered = [m for m in self.messages if not term or term in m.sender.lower() or term in m.text.lower()]
        self.tree.delete(*self.tree.get_children())
        for m in self.filtered:
            self.tree.insert("", "end", values=(m.date, m.time, m.sender, m.text.replace("\n", " ↵ ")))
        self._show_stats()

    def _show_stats(self):
        data = statistics(self.filtered)
        lines = [f"MESSAGES      {data['messages']}", f"PARTICIPANTS  {data['participants']}", "", "BY SENDER"]
        lines += [f"  {name}: {count}" for name, count in data["senders"].most_common()]
        lines += ["", "TOP WORDS"] + [f"  {word}: {count}" for word, count in data["top_words"]]
        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", "end")
        self.stats_text.insert("1.0", "\n".join(lines))
        self.stats_text.configure(state="disabled")

    def export_csv(self):
        if not self.filtered:
            messagebox.showinfo("Nothing to export", "Import a chat first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            with open(path, "w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.writer(handle)
                writer.writerow(["Date", "Time", "Sender", "Message"])
                writer.writerows((m.date, m.time, m.sender, m.text) for m in self.filtered)
            self.status.set(f"EXPORTED {len(self.filtered)} ROWS")

    def run(self):
        self.root.mainloop()
