import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import threading
import shutil
import tempfile
import re

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PDFConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Conversor de PDF para TIF v1.7")
        self.geometry("700x600")
        self.resizable(False, False)
        self.pdf_files = []
        self.output_folder = ""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        selection_frame = ctk.CTkFrame(main_frame)
        selection_frame.pack(pady=10, padx=10, fill="x")
        self.select_files_button = ctk.CTkButton(selection_frame, text="1. Selecionar Arquivos PDF", command=self.select_pdf_files, height=40)
        self.select_files_button.pack(pady=10, padx=10, fill="x")
        self.file_list_box = ctk.CTkTextbox(selection_frame, height=150)
        self.file_list_box.pack(pady=5, padx=10, fill="x")
        self.file_list_box.insert("0.0", "Nenhum arquivo selecionado.")
        self.file_list_box.configure(state="disabled")
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(pady=10, padx=10, fill="x")
        self.select_output_button = ctk.CTkButton(output_frame, text="2. Selecionar Pasta de Destino", command=self.select_output_folder, height=40)
        self.select_output_button.pack(pady=10, padx=10, fill="x")
        path_frame = ctk.CTkFrame(output_frame)
        path_frame.pack(fill="x", expand=True, pady=(5,0))
        self.output_folder_label = ctk.CTkLabel(path_frame, text="Pasta de destino ainda não selecionada.", wraplength=450, justify="left")
        self.output_folder_label.pack(side="left", fill="x", expand=True, padx=5)
        self.open_folder_button = ctk.CTkButton(path_frame, text="Abrir Pasta", command=self.open_output_folder, state="disabled", width=100)
        self.open_folder_button.pack(side="left", padx=(5, 10))
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(pady=10, padx=10, fill="x")
        settings_label = ctk.CTkLabel(settings_frame, text="Estrutura de Diretórios:", font=ctk.CTkFont(weight="bold"))
        settings_label.pack(side="left", padx=(10, 15))
        self.padding_combobox = ctk.CTkComboBox(settings_frame, values=["8 dígitos (Padrão ONR)", "6 dígitos"])
        self.padding_combobox.set("8 dígitos (Padrão ONR)")
        self.padding_combobox.pack(side="left", expand=True, fill="x", padx=(0, 10))
        process_frame = ctk.CTkFrame(main_frame)
        process_frame.pack(pady=10, padx=10, fill="x")
        self.start_button = ctk.CTkButton(process_frame, text="3. Iniciar Conversão", command=self.start_conversion_thread, state="disabled", height=40, fg_color="green", hover_color="darkgreen")
        self.start_button.pack(pady=10, padx=10, fill="x")
        self.progress_bar = ctk.CTkProgressBar(process_frame)
        self.progress_bar.pack(pady=10, padx=10, fill="x")
        self.progress_bar.set(0)
        self.status_label = ctk.CTkLabel(process_frame, text="Aguardando arquivos e pasta de destino...")
        self.status_label.pack(pady=5)
        self.check_dependencies()

    def check_dependencies(self):
        if not shutil.which("magick"):
            messagebox.showerror("Erro de Dependência", "ImageMagick não foi encontrado!\nPor favor, execute o instalador completo do programa.")
            self.destroy()

    def select_pdf_files(self):
        selected_files = filedialog.askopenfilenames(title="Selecione os arquivos PDF", filetypes=(("PDF Files", "*.pdf"), ("All files", "*.*")))
        if not selected_files: return
        invalid_files = []
        for file_path in selected_files:
            file_name = os.path.basename(file_path)
            if "(" in file_name or ")" in file_name:
                invalid_files.append(file_name)
        if invalid_files:
            error_message = "ERRO: Os seguintes arquivos contêm parênteses '()' no nome, o que não é permitido.\n\nPor favor, renomeie os arquivos e tente novamente:\n\n- " + "\n- ".join(invalid_files)
            messagebox.showerror("Arquivos com Nomes Inválidos", error_message)
            self.pdf_files = []
        else:
            self.pdf_files = selected_files
        self.update_file_list_ui()
        self.update_start_button_state()

    def update_file_list_ui(self):
        self.file_list_box.configure(state="normal")
        self.file_list_box.delete("0.0", "end")
        if self.pdf_files:
            for file in self.pdf_files: self.file_list_box.insert("end", os.path.basename(file) + "\n")
            self.status_label.configure(text=f"{len(self.pdf_files)} arquivo(s) selecionado(s).")
        else:
            self.file_list_box.insert("0.0", "Nenhum arquivo selecionado.")
        self.file_list_box.configure(state="disabled")

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory(title="Selecione a pasta de destino para os TIFs")
        if self.output_folder:
            self.output_folder_label.configure(text=f"Destino: {self.output_folder}")
            self.open_folder_button.configure(state="normal")
        else:
            self.output_folder_label.configure(text="Pasta de destino ainda não selecionada.")
            self.open_folder_button.configure(state="disabled")
        self.update_start_button_state()

    def open_output_folder(self):
        if self.output_folder and os.path.exists(self.output_folder):
            os.startfile(self.output_folder)
        else:
            messagebox.showerror("Erro", "A pasta de destino não foi selecionada ou não existe mais.")

    def update_start_button_state(self):
        if self.pdf_files and self.output_folder: self.start_button.configure(state="normal")
        else: self.start_button.configure(state="disabled")

    def start_conversion_thread(self):
        self.start_button.configure(state="disabled")
        self.select_files_button.configure(state="disabled")
        self.select_output_button.configure(state="disabled")
        thread = threading.Thread(target=self.process_files)
        thread.start()

    def process_files(self):
        self.progress_bar.set(0)
        general_warnings = []
        increment_warnings = []
        total_files = len(self.pdf_files)
        selected_padding = self.padding_combobox.get()
        pad_length = 8 if "8 dígitos" in selected_padding else 6
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, pdf_path in enumerate(self.pdf_files):
                file_name = os.path.basename(pdf_path)
                base_name, _ = os.path.splitext(file_name)
                self.status_label.configure(text=f"Processando: {file_name} ({i+1}/{total_files})")
                numeric_part_match = re.match(r'^\d+', base_name)
                if not numeric_part_match:
                    general_warnings.append(f"AVISO: Arquivo '{file_name}' ignorado (nome não começa com um número).")
                    self.progress_bar.set((i + 1) / total_files)
                    continue
                try:
                    numeric_part_str = numeric_part_match.group(0)
                    matricula_num = int(numeric_part_str)
                    folder_index = (matricula_num - 1) // 1000
                    folder_name = f"{folder_index:0{pad_length}d}"
                    final_folder_path = os.path.join(self.output_folder, folder_name)
                    os.makedirs(final_folder_path, exist_ok=True)
                    suffix = base_name[len(numeric_part_str):]
                    padded_numeric_part = f"{matricula_num:0{pad_length}d}"
                    formatted_base_name = padded_numeric_part + suffix
                    start_page_number = 1
                    max_existing_page = 0
                    pattern = re.compile(re.escape(formatted_base_name) + r'\.(\d{4})\.tif$')
                    for existing_file in os.listdir(final_folder_path):
                        match = pattern.match(existing_file)
                        if match:
                            page_num = int(match.group(1))
                            if page_num > max_existing_page:
                                max_existing_page = page_num
                    if max_existing_page > 0:
                        start_page_number = max_existing_page + 1
                        warning_msg = f"ATENÇÃO: Foi encontrada uma matrícula igual na pasta destino, e foram incrementadas páginas na pasta. Por favor verifique mudança na pasta de número {folder_name} da matrícula {base_name}"
                        increment_warnings.append(warning_msg)
                    temp_output_path = os.path.join(temp_dir, "page-%d.tif")
                    command = [
                        "magick",
                        "-density", "200x200", pdf_path,
                        "-colorspace", "Gray", "-dither", "FloydSteinberg",
                        "-type", "Bilevel", "-compress", "LZW",
                        temp_output_path
                    ]
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    subprocess.run(command, check=True, startupinfo=startupinfo, capture_output=True, text=True)
                    extracted_pages = sorted(os.listdir(temp_dir))
                    for page_index, temp_file_name in enumerate(extracted_pages):
                        page_number = start_page_number + page_index
                        final_file_name = f"{formatted_base_name}.{page_number:04d}.tif"
                        final_file_path = os.path.join(final_folder_path, final_file_name)
                        source_temp_file = os.path.join(temp_dir, temp_file_name)
                        shutil.move(source_temp_file, final_file_path)
                except subprocess.CalledProcessError as e:
                    general_warnings.append(f"ERRO ao converter '{file_name}': {e.stderr}")
                except Exception as e:
                    general_warnings.append(f"ERRO inesperado ao processar '{file_name}': {str(e)}")
                self.progress_bar.set((i + 1) / total_files)
        
        final_report = []
        if increment_warnings:
            final_report.append("--- RELATÓRIO DE INCREMENTAÇÃO ---")
            final_report.extend(increment_warnings)
        if general_warnings:
            if final_report: final_report.append("\n--- OUTROS AVISOS E ERROS ---")
            final_report.extend(general_warnings)
        
        if final_report:
            messagebox.showwarning("Relatório de Conversão", "\n".join(final_report))
        else:
            messagebox.showinfo("Sucesso", "Todos os arquivos foram convertidos com sucesso!")
        
        self.pdf_files = []
        self.update_file_list_ui()
        self.status_label.configure(text="Aguardando arquivos e pasta de destino...")
        self.update_start_button_state()
        self.start_button.configure(state="normal")
        self.select_files_button.configure(state="normal")
        self.select_output_button.configure(state="normal")

if __name__ == "__main__":
    app = PDFConverterApp()
    app.mainloop()