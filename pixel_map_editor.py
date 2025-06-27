import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image

# Configurações iniciais
default_rows = 20
default_cols = 20
default_cell_size = 25

# Cores e seus significados
COLORS = {
    'Parede': ((0, 0, 0), '#000000'),
    'Espaço vazio': ((255, 255, 255), '#FFFFFF'),
    'Tapete/Caminho': ((255, 165, 0), '#FFA500'),
    'Inocupável': ((128, 128, 128), '#808080'),
}

class PixelMapEditor(tk.Tk):
    def __init__(self, rows=default_rows, cols=default_cols, cell_size=default_cell_size):
        super().__init__()
        self.title('Editor de Mapas Pixel Art')
        self.resizable(False, False)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.selected_color_name = 'Parede'
        self.selected_rgb, self.selected_hex = COLORS[self.selected_color_name]
        self.map = [[(255, 255, 255) for _ in range(cols)] for _ in range(rows)]
        self._build_ui()
        self._draw_map()

    def _build_ui(self):
        # Frame para seleção de cor
        color_frame = tk.Frame(self)
        color_frame.pack(pady=5)
        tk.Label(color_frame, text='Selecione a cor:').pack(side=tk.LEFT)
        self.color_buttons = {}
        for name, (rgb, hex_color) in COLORS.items():
            btn = tk.Button(color_frame, bg=hex_color, width=3, relief=tk.SUNKEN if name==self.selected_color_name else tk.RAISED,
                            command=lambda n=name: self._select_color(n))
            btn.pack(side=tk.LEFT, padx=2)
            self.color_buttons[name] = btn

        # Canvas para o mapa
        self.canvas = tk.Canvas(self, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg='white')
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind('<Button-1>', self._on_canvas_click)
        self.canvas.bind('<B1-Motion>', self._on_canvas_click)

        # Botão de salvar
        save_btn = tk.Button(self, text='Salvar como PNG', command=self._save_as_png)
        save_btn.pack(pady=5)

    def _select_color(self, name):
        self.selected_color_name = name
        self.selected_rgb, self.selected_hex = COLORS[name]
        for n, btn in self.color_buttons.items():
            btn.config(relief=tk.SUNKEN if n==name else tk.RAISED)

    def _on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.map[row][col] = self.selected_rgb
            self._draw_cell(row, col)

    def _draw_map(self):
        self.canvas.delete('all')
        for row in range(self.rows):
            for col in range(self.cols):
                self._draw_cell(row, col)

    def _draw_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        color = '#%02x%02x%02x' % self.map[row][col]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

    def _save_as_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
        if not file_path:
            return
        img = Image.new('RGB', (self.cols, self.rows))
        for y in range(self.rows):
            for x in range(self.cols):
                img.putpixel((x, y), self.map[y][x])
        try:
            img.save(file_path)
            messagebox.showinfo('Sucesso', f'Mapa salvo em {file_path}')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível salvar: {e}')

if __name__ == '__main__':
    # Janela para configuração inicial
    def start_editor():
        try:
            rows = int(row_var.get())
            cols = int(col_var.get())
            cell_size = int(cell_size_var.get())
            config_win.destroy()
            app = PixelMapEditor(rows, cols, cell_size)
            app.mainloop()
        except Exception as e:
            messagebox.showerror('Erro', f'Valores inválidos: {e}')

    config_win = tk.Tk()
    config_win.title('Configuração do Mapa')
    tk.Label(config_win, text='Linhas:').grid(row=0, column=0)
    tk.Label(config_win, text='Colunas:').grid(row=1, column=0)
    tk.Label(config_win, text='Tamanho da célula (px):').grid(row=2, column=0)
    row_var = tk.StringVar(value=str(default_rows))
    col_var = tk.StringVar(value=str(default_cols))
    cell_size_var = tk.StringVar(value=str(default_cell_size))
    tk.Entry(config_win, textvariable=row_var, width=5).grid(row=0, column=1)
    tk.Entry(config_win, textvariable=col_var, width=5).grid(row=1, column=1)
    tk.Entry(config_win, textvariable=cell_size_var, width=5).grid(row=2, column=1)
    tk.Button(config_win, text='Iniciar Editor', command=start_editor).grid(row=3, column=0, columnspan=2, pady=5)
    config_win.mainloop() 