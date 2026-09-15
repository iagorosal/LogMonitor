import os
from time import sleep
import tkinter as tk
from tkinter import filedialog, scrolledtext

class Logmain():
    def __init__(self, root):
        self.root = root
        self.root.title = "SuriLog Monitorador"
        self.root.geometry("1090x800")
        self.root.resizable(False, False)

        #Guardar o caminho do Log a ser aberto
        self.caminho_arquivo = None
        self.arquivo_aberto = None

        #Arquivos de janela, botão procurar LOG
        self.btn_select = tk.Button(root, text="Open File", command=self.open_file, font=("arial", 12))
        self.btn_select.pack(pady=5)

        #Mostrar o caminho do arquivo selecionado
        self.lbl_arquivo = tk.Label(root, text="Nenhum Arquivo Selecionado", fg="gray", font=("Arial",9,"italic"))
        self.lbl_arquivo.pack(pady=5)

        #Scroll automatico
        self.txt_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#1e1e1e", fg="#ffffff", font=("Consolas",10))
        self.txt_log.pack(expand=True, fill="both", padx=10, pady=10)

        #Fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def open_file(self):
        #Para abrir a janela para selecionar o arquivo
        select_arch = filedialog.askopenfilename(
            title="Selecione o Arquivo de Log",
            filetypes=[("Arquivos de log","*.log *.txt"), ("Todos os arquivos", "*.*")]
        )
        if select_arch:
            #Caso tenha um arquivo aberto, fecha o anterior e abre o novo
            if self.arquivo_aberto:
                self.arquivo_aberto.close()

            self.caminho_arquivo = select_arch
            self.lbl_arquivo.config(text=f"Monitorando: {os.path.basename(select_arch)}", fg="green")

            #Limpa a tela
            self.txt_log.delete(1.0, tk.END)
            self.txt_log.insert(tk.END, f"--- Iniciando leitura do Arquivo: {select_arch} --- \n\n")

            #abre o novo arquivo
            self.arquivo_aberto = open(self.caminho_arquivo, "r", encoding="utf-8", errors="ignore")

            #self.arquivo_aberto.seek(0, os.SEEK_END)

            #Inicia o Loop de verificação em tempo real
            self.atualizar_log()

    def atualizar_log(self):
        #Se houver um arquivo aberto, ira ler a proxima linha
        if self.arquivo_aberto:
            linha = self.arquivo_aberto.readline()

            if linha:
                #inserir a linha no fim do arquivo
                self.txt_log.insert(tk.END, linha)
                #faz o scroll para descer para o final
                self.txt_log.see(tk.END)

                self.root.after(1, self.atualizar_log)
                return
        #se não houver nvoas linhas, ele espera 100 ms para tentar novamente
        self.root.after(100, self.atualizar_log)

    def close_window(self):
        if self.arquivo_aberto:
            self.arquivo_aberto.close()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app =  Logmain(root)
    root.mainloop()





