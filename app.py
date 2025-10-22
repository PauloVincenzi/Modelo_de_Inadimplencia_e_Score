import os, sys
import pickle
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from scipy.special import logit


# ============================================
# 1 - Encontrar o path
# ============================================

def resource_path(relative_path):
    """
    Garante que arquivos externos (ex: modelos .pkl) sejam encontrados
    tanto quando o código é executado em Python quanto no executável (.exe).
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ============================================
# 2 - Carregar modelo e pré-processamento
# ============================================
logreg = pickle.load(open(resource_path('modelos/modelo_credito.pkl'), 'rb'))
scaler = pickle.load(open(resource_path('modelos/scaler.pkl'), 'rb'))
num_cols = pickle.load(open(resource_path('modelos/num_cols.pkl'), 'rb'))
cols_modelo = pickle.load(open(resource_path('modelos/cols_modelo.pkl'), 'rb'))


# ============================================
# 3 - Função de variáveis derivadas
# ============================================
def variaveis_derivadas(df):
    bill_cols = ['BILL_AMT1','BILL_AMT2','BILL_AMT3','BILL_AMT4','BILL_AMT5','BILL_AMT6']
    pay_cols = ['PAY_AMT1','PAY_AMT2','PAY_AMT3','PAY_AMT4','PAY_AMT5','PAY_AMT6']
    pay_status = ['PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6']

    df['Credit_per_Age'] = df['LIMIT_BAL'] / (df['AGE'] + 1)
    df['BILL_MEAN'] = df[bill_cols].mean(axis=1)
    df['BILL_STD'] = df[bill_cols].std(axis=1)
    df['BILL_TREND'] = df[bill_cols].iloc[:, 0] - df[bill_cols].iloc[:, -1]
    df['PAY_MEAN'] = df[pay_cols].mean(axis=1)
    df['PAY_STD'] = df[pay_cols].std(axis=1)
    df['PAY_TREND'] = df[pay_cols].iloc[:, 0] - df[pay_cols].iloc[:, -1]
    df['PAY_to_BILL_MEAN'] = df['PAY_MEAN'] / (df['BILL_MEAN'] + 1)
    df['PAY_to_LIMIT'] = df['PAY_MEAN'] / (df['LIMIT_BAL'] + 1)
    df['BILL_to_LIMIT'] = df['BILL_MEAN'] / (df['LIMIT_BAL'] + 1)
    # MAX_DELAY e MEAN_DELAY foram removidos, pois não é mais usado no modelo final
    df['N_DELAY'] = (df[pay_status] > 0).sum(axis=1)
    df['ANY_DELAY'] = (df[pay_status] > 0).any(axis=1).astype(int)
    df['HIGH_UTILIZATION'] = (df['BILL_to_LIMIT'] > 0.8).astype(int)
    df['LOW_PAYMENT_RATIO'] = (df['PAY_to_BILL_MEAN'] < 0.5).astype(int)

    return df


# ============================================
# 4 - Função calcular score
# ============================================
def calcular_score():
    try:
        # Coletar limite de crédito e idade
        limit_bal_val = float(limit_bal_entry.get())
        age_val = float(age_entry.get())

        # Montar listas com os dados coletados em cada mês
        pay_vals = [pay_map[c.get()] for c in pay_entries]
        bill_vals = [float(c.get()) for c in bill_entries]
        pay_amt_vals = [float(c.get()) for c in pay_amt_entries]

        # Montar dados do cliente
        dados = {
                'LIMIT_BAL':[limit_bal_val],
                'AGE':[age_val],
                'SEX':[sex_map[sex_combo.get()]],
                'EDUCATION':[edu_map[edu_combo.get()]],
                'MARRIAGE':[marriage_map[marriage_combo.get()]],

                'PAY_0':[pay_vals[5]],
                'PAY_2':[pay_vals[4]],
                'PAY_3':[pay_vals[3]],
                'PAY_4':[pay_vals[2]],
                'PAY_5':[pay_vals[1]],
                'PAY_6':[pay_vals[0]],

                'BILL_AMT1':[bill_vals[5]],
                'BILL_AMT2':[bill_vals[4]],
                'BILL_AMT3':[bill_vals[3]],
                'BILL_AMT4':[bill_vals[2]],
                'BILL_AMT5':[bill_vals[1]],
                'BILL_AMT6':[bill_vals[0]],

                'PAY_AMT1':[pay_amt_vals[5]],
                'PAY_AMT2':[pay_amt_vals[4]],
                'PAY_AMT3':[pay_amt_vals[3]],
                'PAY_AMT4':[pay_amt_vals[2]],
                'PAY_AMT5':[pay_amt_vals[1]],
                'PAY_AMT6':[pay_amt_vals[0]],
            }

        # Transformar dados em dataframe.
        df_user = pd.DataFrame(dados)

        # Gerar features derivadas
        df_user = variaveis_derivadas(df_user)

        # Dummies em categoricas
        df_user = pd.get_dummies(df_user, drop_first=True)

        # Garantir que todas as colunas do modelo existam
        for col in cols_modelo:
            if col not in df_user.columns:
                df_user[col] = 0
        df_user = df_user[cols_modelo]

        # Padronizar variáveis numéricas
        df_user[num_cols] = scaler.transform(df_user[num_cols])

        # Probabilidade e score
        y_prob = logreg.predict_proba(df_user)[:,1]
        epsilon = 1e-6
        y_prob = np.clip(y_prob, epsilon, 1-epsilon)
        base_score = 600
        factor = 50
        score = base_score + factor*logit(1 - y_prob)
        score = np.clip(score, 300, 850).astype(int)

        # Mostrar resultado
        messagebox.showinfo("Resultado", f"Probabilidade inadimplência: {(y_prob[0]*100):.1f} %\nScore: {score[0]}")
    except Exception as e:
        # Caso algo seja preenchido incorretamente, retorna o erro dado
        messagebox.showerror("Erro", f"Erro: {str(e)}")


# ============================================
# 5 - Criar interface gráfica e interativa
# ============================================

cor_fundo = '#c5d0f0'
cor_mes = '#d1c4e9'

root = tk.Tk()
root.title("Calculadora de Score de Crédito")
root.geometry("1200x650")
root.configure(bg=cor_fundo)

# Cabeçalho
header_frame = tk.Frame(root, bg="#4b6cb7", pady=15)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Calculadora de Score de Crédito", 
                        font=("Arial", 20, "bold"), fg="white", bg="#4b6cb7")
header_label.pack()

# Subcabeçalho
subheader_frame = tk.Frame(root, bg=cor_fundo, pady=20)
subheader_frame.pack(fill="x")
subheader_label = tk.Label(subheader_frame, text="Suponha que você possua um cartão de crédito com limite definido.\nPreencha as informações referentes às suas últimas 6 faturas, incluindo quanto devia e quanto pagou em cada mês.\nO sistema irá estimar a probabilidade de inadimplência e calcular seu score de crédito.", 
                           font=("Arial", 14), bg=cor_fundo)
subheader_label.pack()


# Topo (LIMIT_BAL, AGE, SEX, EDUCATION, MARRIAGE)
top_frame = tk.Frame(root, bg=cor_fundo)
top_frame.pack(pady=10)

# LIMIT_BAL
tk.Label(top_frame, text="Valor do seu limite de crédito", bg=cor_fundo, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=40, pady=5)
limit_bal_entry = tk.Entry(top_frame, width=12)
limit_bal_entry.grid(row=1, column=0, padx=40, pady=5)

# AGE
tk.Label(top_frame, text="Idade", bg=cor_fundo, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=40, pady=5)
age_entry = tk.Entry(top_frame, width=5)
age_entry.grid(row=1, column=1, padx=40, pady=5)

# SEX
sex_map = {'': '','Masculino': 1, 'Feminino': 2}
tk.Label(top_frame, text="Sexo", bg=cor_fundo, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=40, pady=5)
sex_combo = ttk.Combobox(top_frame, values=list(sex_map.keys()), state="readonly", width=12)
sex_combo.grid(row=1, column=2, padx=40, pady=5)
sex_combo.current(0)

# EDUCATION
edu_map = {"": "", "Ensino Médio": 1, "Graduação": 2, "Pós Graduação": 3, "Outro": 4}
tk.Label(top_frame, text="Educação", bg=cor_fundo, font=("Arial", 10, "bold")).grid(row=0, column=3, padx=40, pady=5)
edu_combo = ttk.Combobox(top_frame, values=list(edu_map.keys()), state="readonly", width=15)
edu_combo.grid(row=1, column=3, padx=40, pady=5)
edu_combo.current(0)

# MARRIAGE
marriage_map = {"": "", "Casado": 1, "Solteiro": 2, "Outro": 3}
tk.Label(top_frame, text="Estado Civil", bg=cor_fundo, font=("Arial", 10, "bold")).grid(row=0, column=4, padx=40, pady=5)
marriage_combo = ttk.Combobox(top_frame, values=list(marriage_map.keys()), state="readonly", width=12)
marriage_combo.grid(row=1, column=4, padx=40, pady=5)
marriage_combo.current(0)


# Seis colunas, cada coluna: PAY, BILL_AMT, PAY_AMT
month_frame = tk.Frame(root, bg=cor_fundo)
month_frame.pack(pady=10)

pay_entries = []
bill_entries = []
pay_amt_entries = []

pay_map = {
    "Sem fatura": -2,
    "Pagamento em dia": -1,
    "Em dia (crédito rotativo)": 0,
    "Atraso 1 mês": 1,
    "Atraso 2 meses": 2,
    "Atraso 3 meses": 3,
    "Atraso 4 meses": 4,
    "Atraso 5 meses": 5,
    "Atraso 6 meses": 6,
    "Atraso 7 meses": 7,
    "Atraso 8 meses": 8,
    "Atraso 9 meses ou mais": 9
}

for month in range(6):
    col_frame = tk.Frame(month_frame, bd=1, relief="solid", padx=5, pady=5, 
                         bg=cor_mes, highlightbackground="#b39ddb", highlightthickness=2)
    col_frame.grid(row=0, column=month, padx=5)

    if month == 5:
        tk.Label(col_frame, text=f"Mês anterior", bg=cor_mes, font=("Arial", 10, "bold")).pack()
    else:
        tk.Label(col_frame, text=f"{6-month} meses atrás", bg=cor_mes, font=("Arial", 10, "bold")).pack()

    # PAY
    tk.Label(col_frame, text="Atraso na fatura", bg=cor_mes).pack()
    pay_combo = ttk.Combobox(col_frame, values=list(pay_map.keys()), state="readonly", width=25)
    pay_combo.pack()
    pay_combo.current(0)
    pay_entries.append(pay_combo)

    # BILL_AMT
    tk.Label(col_frame, text="Saldo devido", bg=cor_mes).pack()
    bill_entry = tk.Entry(col_frame, width=12)
    bill_entry.pack()
    bill_entries.append(bill_entry)

    # PAY_AMT
    tk.Label(col_frame, text="Saldo pago", bg=cor_mes).pack()
    pay_amt_entry = tk.Entry(col_frame, width=12)
    pay_amt_entry.pack()
    pay_amt_entries.append(pay_amt_entry)


# Botão calcular score
btn_calc = tk.Button(root, text="Calcular Score", command=calcular_score,
                     bg="#4b6cb7", fg="white", font=("Arial", 14, "bold"), padx=20, pady=10)
btn_calc.pack(pady=20)


# ============================================
# 6 - Mantém a janela interativa aberta
# ============================================
root.mainloop()
