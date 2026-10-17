# -*- coding: utf-8 -*-
import os
import json
import streamlit as st
from PIL import Image as PILImage, ImageDraw
import pandas as pd

st.set_page_config(page_title="Sistema Financeiro - AD Belém", layout="wide")

caminho_logo = "logo_igreja.png"
arquivo_senhas_config = "config_senhas_acesso.json"

SENHAS_PADRAO_INICIAIS = {
    "Presidente": "PRESIDENTE2026*",
    "Primeiro-Tesoureiro": "TESOURARIA1*",
    "Segundo-Tesoureiro": "TESOURARIA2*",
    "Comissão de Contas": "COMISSAO2026*"
}

def carregar_senhas_salvas():
    if os.path.exists(arquivo_senhas_config):
        try:
            with open(arquivo_senhas_config, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return SENHAS_PADRAO_INICIAIS.copy()

def salvar_senhas_disco(dic_senhas):
    with open(arquivo_senhas_config, 'w', encoding='utf-8') as f:
        json.dump(dic_senhas, f, ensure_ascii=False, indent=4)

if 'senhas_adm' not in st.session_state:
    st.session_state['senhas_adm'] = carregar_senhas_salvas()

def criar_logo_padrao():
    img = PILImage.new('RGB', (150, 150), color=(26, 54, 93))
    d = ImageDraw.Draw(img)
    d.rectangle([5, 5, 145, 145], outline=(255, 255, 255), width=2)
    d.text((35, 65), "AD BELÉM", fill=(255, 255, 255))
    img.save(caminho_logo, format="PNG")

if not os.path.exists(caminho_logo):
    criar_logo_padrao()

SENHAS_FILIAIS = {
    "01 - Altinópolis": "QF5821",
    "02 - Batatais (Anselmo Testa)": "MR7306",
    "03 - Batatais (Vila Maria)": "TK1948",
    "04 - Brodowski": "ZP6253",
    "05 - Central": "HW8417",
    "06 - Cravinhos": "BN3069",
    "07 - Cristo Redentor": "LX5724",
    "08 - Heitor Rigon": "CJ9185",
    "09 - Jd. Marchesi": "VD4630",
    "10 - Morro Agudo (Inácio Franco)": "RK2571",
    "11 - Orestes Lopes": "FG8042",
    "12 - Parque Ribeirão": "WY1367",
    "13 - Piratininga": "SP6924",
    "14 - Ribeirão Verde": "DA3758",
    "15 - Serra Azul": "NM5206",
    "16 - Serrana": "XB7481",
    "17 - Servidores": "PU2095",
    "18 - Vila Virgínia": "GE6813"
}

MESES_DO_ANO = {
    "01 - Janeiro": "01", "02 - Fevereiro": "02", "03 - Março": "03", "04 - Abril": "04",
    "05 - Maio": "05", "06 - Junho": "06", "07 - Julho": "07", "08 - Agosto": "08",
    "09 - Setembro": "09", "10 - Outubro": "10", "11 - Novembro": "11", "12 - Dezembro": "12"
}

# Interface Streamlit
st.title("🏛️ Sistema Financeiro - AD Belém")

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.subheader("Login de Acesso")
    perfil_sel = st.selectbox("Perfil de Acesso:", ['Presidente', 'Primeiro-Tesoureiro', 'Segundo-Tesoureiro', 'Comissão de Contas', 'Tesoureiro Local'])
    cong_sel = st.selectbox("Congregação:", list(SENHAS_FILIAIS.keys()))
    senha_input = st.text_input("Senha:", type="password")
    ano_input = st.text_input("Ano de Referência:", value="2026")

    if st.button("Entrar"):
        senhas_adm = st.session_state['senhas_adm']
        if perfil_sel in ['Presidente', 'Primeiro-Tesoureiro', 'Segundo-Tesoureiro', 'Comissão de Contas']:
            if senha_input == senhas_adm.get(perfil_sel, ""):
                st.session_state['autenticado'] = True
                st.session_state['perfil'] = perfil_sel
                st.session_state['congregacao'] = cong_sel
                st.session_state['ano'] = ano_input
                st.session_state['eh_amplo'] = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta para este cargo.")
        elif perfil_sel == 'Tesoureiro Local':
            if senha_input == SENHAS_FILIAIS.get(cong_sel, ""):
                st.session_state['autenticado'] = True
                st.session_state['perfil'] = perfil_sel
                st.session_state['congregacao'] = cong_sel
                st.session_state['ano'] = ano_input
                st.session_state['eh_amplo'] = False
                st.rerun()
            else:
                st.error("❌ Senha incorreta para esta congregação.")
else:
    perfil = st.session_state['perfil']
    congregacao = st.session_state['congregacao']
    ano = st.session_state['ano']
    eh_amplo = st.session_state['eh_amplo']

    st.sidebar.markdown(f"**Logado como:** {perfil}")
    st.sidebar.markdown(f"**Filial:** {congregacao}")
    if st.sidebar.button("🚪 Sair"):
        st.session_state['autenticado'] = False
        st.rerun()

    menu = st.sidebar.radio("Navegação", ["Lançamentos Mensais", "Relatório Geral do Mês", "Demonstrativo Anual", "Gerenciar Senhas"])

    if menu == "Lançamentos Mensais":
        st.header(f"Balancete: {congregacao} ({ano})")
        mes_nome = st.selectbox("Selecione o Mês:", list(MESES_DO_ANO.keys()))
        num_mes = MESES_DO_ANO[mes_nome]
        mes_ano_str = f"{mes_nome.split(' - ')[1]}/{ano}"

        nome_arquivo_json = f"dados_{congregacao.replace(' ', '_').replace('/', '_')}_{num_mes}_{ano}.json"

        dados_salvos = {"dirigente": "", "tesoureiro": "", "entradas": [], "despesas": []}
        if os.path.exists(nome_arquivo_json):
            try:
                with open(nome_arquivo_json, 'r', encoding='utf-8') as f:
                    dados_salvos = json.load(f)
            except Exception:
                pass

        dirigente = st.text_input("Dirigente Local:", value=dados_salvos["dirigente"])
        tesoureiro = st.text_input("Tesoureiro Local:", value=dados_salvos["tesoureiro"])

        st.markdown("---")
        st.subheader("➕ Adicionar Receita (Entrada)")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: dia_rec = st.text_input("Dia Culto", placeholder="15")
        with col2: talao = st.text_input("Talão", placeholder="TL-01")
        with col3: nome_memb = st.text_input("Nome do Membro")
        with col4: tipo_ent = st.selectbox("Tipo", ['Dízimo', 'Oferta', 'Outros'])
        with col5: forma_ent = st.selectbox("Forma", ['Espécie', 'PIX'])
        
        col6, col7 = st.columns(2)
        with col6: espec_ent = st.text_input("Observação / Especificação", value="Dízimo Mensal")
        with col7: valor_ent = st.number_input("Valor (R$)", min_value=0.0, step=0.10, format="%.2f")

        if st.button("Adicionar Entrada"):
            if dia_rec and nome_memb and valor_ent > 0:
                nova_ent = {
                    "data": f"{dia_rec.zfill(2)}/{num_mes}/{ano}",
                    "talao": talao or "N/D",
                    "nome": nome_memb,
                    "tipo": tipo_ent,
                    "forma": forma_ent,
                    "especificacao": espec_ent,
                    "valor": valor_ent
                }
                dados_salvos["entradas"].append(nova_ent)
                dados_salvos["dirigente"] = dirigente
                dados_salvos["tesoureiro"] = tesoureiro
                with open(nome_arquivo_json, 'w', encoding='utf-8') as f:
                    json.dump(dados_salvos, f, ensure_ascii=False, indent=4)
                st.success("Entrada adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha o dia, nome e valor da entrada.")

        st.markdown("---")
        st.subheader("💸 Adicionar Despesa (Saída)")
        col1, col2, col3, col4 = st.columns(4)
        with col1: dia_desp = st.text_input("Dia Despesa", placeholder="10", key="d_desp")
        with col2: tipo_desp = st.selectbox("Tipo Despesa", ['Água/Esgoto', 'Energia Elétrica', 'Aluguel', 'Manutenção/Reformas', 'Material de Limpeza', 'Som/Instrumentos', 'Evangelismo/Ação Social', 'Outras Despesas'])
        with col3: desc_desp = st.text_input("Descrição / Favorecido")
        with col4: valor_desp = st.number_input("Valor Despesa (R$)", min_value=0.0, step=0.10, format="%.2f", key="v_desp")

        if st.button("Adicionar Despesa"):
            if dia_desp and valor_desp > 0:
                nova_desp = {
                    "data": f"{dia_desp.zfill(2)}/{num_mes}/{ano}",
                    "tipo": tipo_desp,
                    "descricao": desc_desp or tipo_desp,
                    "valor": valor_desp
                }
                dados_salvos["despesas"].append(nova_desp)
                dados_salvos["dirigente"] = dirigente
                dados_salvos["tesoureiro"] = tesoureiro
                with open(nome_arquivo_json, 'w', encoding='utf-8') as f:
                    json.dump(dados_salvos, f, ensure_ascii=False, indent=4)
                st.success("Despesa adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha o dia e o valor da despesa.")

        tot_ent = sum(i['valor'] for i in dados_salvos["entradas"])
        tot_desp = sum(d['valor'] for d in dados_salvos["despesas"])
        rec_liq = max(0.0, tot_ent - tot_desp)
        prebenda = rec_liq * 0.30
        saldo_cong = tot_ent - tot_desp - prebenda

        st.markdown("---")
        st.subheader("📊 Resumo do Mês")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Entradas Brutas", f"R$ {tot_ent:,.2f}")
        k2.metric("Despesas", f"R$ {tot_desp:,.2f}")
        k3.metric("Prebenda (30%)", f"R$ {prebenda:,.2f}")
        k4.metric("Saldo Líquido (70%)", f"R$ {saldo_cong:,.2f}")

        if dados_salvos["entradas"]:
            st.markdown("### Entradas Registadas")
            df_ent = pd.DataFrame(dados_salvos["entradas"])
            st.dataframe(df_ent, use_container_width=True)

        if dados_salvos["despesas"]:
            st.markdown("### Despesas Registadas")
            df_desp = pd.DataFrame(dados_salvos["despesas"])
            st.dataframe(df_desp, use_container_width=True)

    elif menu == "Relatório Geral do Mês":
        if not eh_amplo:
            st.error("Acesso restrito a perfis administrativos.")
        else:
            st.header(f"📊 Consolidado Geral do Campo - Exercício {ano}")
            tot_g_ent, tot_g_desp, tot_g_preb, tot_g_saldo = 0.0, 0.0, 0.0, 0.0
            
            tabela_dados = []
            for filial in SENHAS_FILIAIS.keys():
                f_limpa = filial.replace(' ', '_').replace('/', '_')
                f_ent, f_desp = 0.0, 0.0
                for _, num_mes in MESES_DO_ANO.items():
                    arq = f"dados_{f_limpa}_{num_mes}_{ano}.json"
                    if os.path.exists(arq):
                        try:
                            with open(arq, 'r', encoding='utf-8') as f:
                                d = json.load(f)
                                f_ent += sum(i['valor'] for i in d.get("entradas", []))
                                f_desp += sum(de['valor'] for de in d.get("despesas", []))
                        except Exception:
                            pass
                if f_ent > 0 or f_desp > 0:
                    f_liq = max(0.0, f_ent - f_desp)
                    f_preb = f_liq * 0.30
                    f_saldo = f_ent - f_desp - f_preb
                    tot_g_ent += f_ent
                    tot_g_desp += f_desp
                    tot_g_preb += f_preb
                    tot_g_saldo += f_saldo
                    tabela_dados.append({"Congregação": filial, "Entradas": f"R$ {f_ent:,.2f}", "Despesas": f"R$ {f_desp:,.2f}", "Prebenda": f"R$ {f_preb:,.2f}", "Saldo": f"R$ {f_saldo:,.2f}"})

            if tabela_dados:
                st.dataframe(pd.DataFrame(tabela_dados), use_container_width=True)
                st.markdown(f"### Totais Gerais: Entradas: R$ {tot_g_ent:,.2f} | Despesas: R$ {tot_g_desp:,.2f} | Prebendas: R$ {tot_g_preb:,.2f} | Saldo: R$ {tot_g_saldo:,.2f}")
            else:
                st.info("Nenhum lançamento registrado no ano.")

    elif menu == "Gerenciar Senhas":
        if not eh_amplo:
            st.error("Acesso restrito.")
        else:
            st.header("🔑 Modificar Senhas de Acesso")
            cargo_alt = st.selectbox("Selecione o Cargo:", ['Presidente', 'Primeiro-Tesoureiro', 'Segundo-Tesoureiro', 'Comissão de Contas'])
            nova_senha_val = st.text_input("Nova Senha:", type="password")
            if st.button("Salvar Nova Senha"):
                if nova_senha_val:
                    st.session_state['senhas_adm'][cargo_alt] = nova_senha_val
                    salvar_senhas_disco(st.session_state['senhas_adm'])
                    st.success(f"Senha do cargo '{cargo_alt}' alterada com sucesso!")
                else:
                    st.warning("Digite uma senha válida.")