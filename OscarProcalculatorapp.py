import tkinter as tk
from tkinter import ttk
import ast
import operator


class SafeEvaluator:
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def evaluate(cls, expression: str) -> float:
        node = ast.parse(expression, mode="eval").body
        return cls._eval_node(node)

    @classmethod
    def _eval_node(cls, node):
        if isinstance(node, ast.Num):  # Python <3.8
            return node.n
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant")
        if isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op_type = type(node.op)
            if op_type not in cls.ALLOWED_OPERATORS:
                raise ValueError("Operator not allowed")
            func = cls.ALLOWED_OPERATORS[op_type]
            return func(left, right)
        if isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            op_type = type(node.op)
            if op_type not in cls.ALLOWED_OPERATORS:
                raise ValueError("Unary operator not allowed")
            func = cls.ALLOWED_OPERATORS[op_type]
            return func(operand)
        if isinstance(node, ast.Expr):
            return cls._eval_node(node.value)
        raise ValueError("Invalid expression")


class CalculatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Oscar's Pro Calculator")
        self.geometry("380x560")
        self.minsize(340, 540)
        self.configure(bg="#0e1420")

        self.expression_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")

        self._build_styles()
        self._build_layout()
        self._bind_keys()

    def _build_styles(self) -> None:
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        # Palette
        self.color_bg = "#0e1420"
        self.color_panel = "#121a28"
        self.color_display = "#0f1926"
        self.color_text = "#e8edf2"
        self.color_muted = "#8fa1b7"
        self.color_digit = "#2b3440"
        self.color_digit_hover = "#323c49"
        self.color_op_orange = "#f97316"
        self.color_op_orange_hover = "#fb923c"
        self.color_action = "#000000"
        self.color_action_hover = "#0a0a0a"
        self.color_btn = "#1e1e2e"
        self.color_btn_hover = "#2a2a3a"

        # Display style
        self.style.configure(
            "Display.TEntry",
            fieldbackground=self.color_display,
            foreground=self.color_text,
            bordercolor=self.color_display,
            lightcolor=self.color_display,
            darkcolor=self.color_display,
            borderwidth=0,
            padding=8,
            relief="flat",
        )
        
        # Button styles to prevent OS override
        self.style.configure(
            "Digit.TButton",
            background="#ffffff",
            foreground="#000000",
            borderwidth=0,
            focuscolor="none",
            padding=(10, 10),
        )
        self.style.map("Digit.TButton",
            background=[("active", "#f0f0f0"), ("pressed", "#ffffff")]
        )
        
        self.style.configure(
            "Op.TButton",
            background="#06b6d4",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="none",
            padding=(10, 10),
        )
        self.style.map("Op.TButton",
            background=[("active", "#0891b2"), ("pressed", "#06b6d4")]
        )
        
        self.style.configure(
            "Action.TButton",
            background="#06b6d4",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="none",
            padding=(10, 10),
        )
        self.style.map("Action.TButton",
            background=[("active", "#0891b2"), ("pressed", "#06b6d4")]
        )

    def _build_layout(self) -> None:
        container = ttk.Frame(self, padding=18)
        container.pack(fill="both", expand=True)
        container.configure(style="Panel.TFrame")
        self.style.configure("Panel.TFrame", background=self.color_bg)

        # Header
        header_frame = tk.Frame(container, bg=self.color_bg)
        header_frame.pack(fill="x")
        accent = tk.Frame(header_frame, bg="#0a1220", height=4)
        accent.pack(fill="x", side="top", pady=(0, 10))
        title = tk.Label(
            header_frame,
            text="Oscar's Pro Calculator",
            anchor="center",
            font=("Helvetica Neue", 16, "bold"),
            bg=self.color_bg,
            fg=self.color_text,
        )
        title.pack(fill="x", pady=(2, 8))

        # Display panel
        card_outer = tk.Frame(container, bg=self.color_bg)
        card_outer.pack(fill="x")
        card_shadow = tk.Frame(card_outer, bg="#0a1220")
        card_shadow.pack(fill="x", padx=2, pady=(0, 14))
        display_frame = tk.Frame(card_shadow, bg=self.color_panel)
        display_frame.pack(fill="x", padx=2, pady=2)

        expression_label = tk.Label(
            display_frame,
            textvariable=self.expression_var,
            anchor="e",
            font=("Helvetica Neue", 12),
            bg=self.color_panel,
            fg=self.color_muted,
        )
        expression_label.pack(fill="x")

        self.display = ttk.Entry(
            display_frame,
            textvariable=self.result_var,
            justify="right",
            font=("Helvetica Neue", 38, "bold"),
            style="Display.TEntry",
        )
        self.display.pack(fill="x", ipady=12, padx=8, pady=(0, 8))
        self.display.configure(state="readonly")

        # Buttons grid
        grid_frame = tk.Frame(container, bg=self.color_bg, highlightthickness=0, bd=0)
        grid_frame.pack(fill="both", expand=True)



        for i in range(6):
            grid_frame.rowconfigure(i, weight=1, uniform="row")
        for j in range(4):
            grid_frame.columnconfigure(j, weight=1, uniform="col")

        buttons = [
            [("C", 1), ("±", 1), ("%", 1), ("⌫", 1)],
            [("7", 1), ("8", 1), ("9", 1), ("÷", 1)],
            [("4", 1), ("5", 1), ("6", 1), ("×", 1)],
            [("1", 1), ("2", 1), ("3", 1), ("−", 1)],
            [("0", 2), (".", 1), ("+", 1)],
            [("=", 4)],
        ]

        for r, row in enumerate(buttons):
            c = 0
            for label, span in row:
                kind = self._button_kind(label)
                # Use ttk.Button with custom styles
                style_name = self._get_button_style(kind)
                btn = ttk.Button(
                    grid_frame,
                    text=label,
                    style=style_name,
                    command=lambda l=label: self._on_press(l)
                )
                btn.grid(row=r, column=c, columnspan=span, padx=7, pady=7, sticky="nsew")

                c += span

    def _bg_for_kind(self, kind: str) -> str:
        if kind == "op":
            return self.color_op_orange
        if kind in ("equals", "action"):
            return self.color_action
        return self.color_btn

    def _hover_for_kind(self, kind: str) -> str:
        if kind == "op":
            return self.color_op_orange_hover
        if kind in ("equals", "action"):
            return self.color_action_hover
        return self.color_btn_hover

    def _get_button_style(self, kind: str) -> str:
        if kind == "op":
            return "Op.TButton"
        if kind in ("equals", "action"):
            return "Action.TButton"
        return "Digit.TButton"

    def _button_kind(self, label: str) -> str:
        if label in {"=",}:
            return "equals"
        if label in {"÷", "×", "−", "+"}:
            return "op"
        if label in {"C", "⌫", "%", "±"}:
            return "action"
        return "digit"

    def _bind_keys(self) -> None:
        self.bind("<Key>", self._on_key)
        self.bind("<Return>", lambda e: self._equals())
        self.bind("=", lambda e: self._equals())
        self.bind("<BackSpace>", lambda e: self._backspace())
        self.bind("<Escape>", lambda e: self._clear())

    def _on_key(self, event: tk.Event) -> None:
        char = event.char
        if char.isdigit() or char == ".":
            self._append_char(char)
            return
        if char in "+-*/":
            self._append_operator(char)
            return

    def _on_press(self, label: str) -> None:
        if label == "C":
            self._clear()
        elif label == "⌫":
            self._backspace()
        elif label == "±":
            self._toggle_sign()
        elif label == "%":
            self._percent()
        elif label == "=":
            self._equals()
        elif label in {"÷", "×", "−", "+"}:
            mapped = {"÷": "/", "×": "*", "−": "-", "+": "+"}[label]
            self._append_operator(mapped)
        else:
            self._append_char(label)

    def _clear(self) -> None:
        self.expression_var.set("")
        self.result_var.set("0")

    def _backspace(self) -> None:
        current = self.expression_var.get()
        if current:
            self.expression_var.set(current[:-1])
        self._reflect_expression_to_result_preview()

    def _toggle_sign(self) -> None:
        expr = self.expression_var.get()
        if not expr:
            return
        i = len(expr) - 1
        while i >= 0 and (expr[i].isdigit() or expr[i] == "."):
            i -= 1
        number = expr[i + 1 :]
        prefix = expr[: i + 1]
        if not number:
            return
        if number.startswith("-"):
            number = number[1:]
        else:
            number = "-" + number
        new_expr = prefix + number
        self.expression_var.set(new_expr)
        self._reflect_expression_to_result_preview()

    def _percent(self) -> None:
        expr = self.expression_var.get()
        if not expr:
            return
        i = len(expr) - 1
        while i >= 0 and (expr[i].isdigit() or expr[i] == "." or (expr[i] == "-" and (i == 0 or not expr[i-1].isdigit()))):
            i -= 1
        number = expr[i + 1 :]
        prefix = expr[: i + 1]
        try:
            value = float(number)
            value /= 100.0
            number_str = ("%f" % value).rstrip("0").rstrip(".")
            self.expression_var.set(prefix + number_str)
            self._reflect_expression_to_result_preview()
        except Exception:
            pass

    def _append_char(self, char: str) -> None:
        expr = self.expression_var.get()
        if char == ".":
            i = len(expr) - 1
            while i >= 0 and (expr[i].isdigit() or expr[i] == "."):
                if expr[i] == ".":
                    return
                i -= 1
        self.expression_var.set(expr + char)
        self._reflect_expression_to_result_preview()

    def _append_operator(self, op: str) -> None:
        expr = self.expression_var.get()
        if not expr and op in "+-*/":
            if op in "+*/":
                return
        if expr.endswith(tuple("+-*/")):
            expr = expr[:-1]
        self.expression_var.set(expr + op)
        self._reflect_expression_to_result_preview()

    def _sanitize_for_eval(self, expr: str) -> str:
        return expr

    def _equals(self) -> None:
        expr = self.expression_var.get()
        if not expr:
            return
        try:
            sanitized = self._sanitize_for_eval(expr)
            result = SafeEvaluator.evaluate(sanitized)
            if int(result) == result:
                pretty = str(int(result))
            else:
                pretty = ("%f" % result).rstrip("0").rstrip(".")
            self.result_var.set(pretty)
        except Exception:
            self.result_var.set("Error")

    def _reflect_expression_to_result_preview(self) -> None:
        expr = self.expression_var.get()
        if not expr:
            self.result_var.set("0")
            return
        try:
            result = SafeEvaluator.evaluate(self._sanitize_for_eval(expr))
            if int(result) == result:
                pretty = str(int(result))
            else:
                pretty = ("%f" % result).rstrip("0").rstrip(".")
            self.result_var.set(pretty)
        except Exception:
            pass


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()