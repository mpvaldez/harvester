# import pandas as pd
# import numpy as np
# import harvester

###############################################
# Santa fe
###############################################

# df = pd.read_csv("data/santa_fe.csv")
# personas = harvester.prepare_entities(df['full_name'].unique())

# data_google = harvester.collect_from_google(personas, 'politico')

# harvester.download(data_google, 'final_santa_fe.csv')


###############################################
# Mergeo de bases
###############################################

# fuente = pd.read_csv("data/fuente.csv")
# elecciones = pd.read_csv("data/elecciones.csv")

# fuente = fuente.rename(columns={'DNI': 'dni'})

# fuente = fuente.drop(columns=[
#     'prioridadCarga', 'distrito', 'estatus', 
#     'alianza', 'cargo', 'subcategoria_cargo',
#     'posicion', 'nombres', 'apellidos',
#     'candidato', 'genero', 'fecha_nacimiento',
#     'otros_partidos', 'twitter', 'user_id', 'status_id', 'location',
#     'description', 'url', 'protected', 'followers_count',    
#     'account_created_at', 'verified', 'profile_url', 'profile_image_url',    
#     'razon_social', 'descripcion_tipo_societario', 'fecha_balance',
#     'cantidad_entidades_igj', 'ORDEN'    
# ])


# df = pd.merge(elecciones, fuente, how="left", on="dni")

# df['profession_1'] = df['profesion']
# df['previous_pubic_roles'] = df['cargos_publicos']
# df['has_descendants'] = df['hijos'].fillna(0).apply(lambda x: "Si" if x>0 else "No")
# df['place_of_birth'] = df['distrito_nacimiento']
# df['URL_photo'] = df['foto_candidato']
# df['URL_TW'] = df['url_twitter']
# df['URL_FB_page'] = df['URL_FB_page_x'].fillna(df['URL_FB_page_y'])
# df['URL_FB_profile'] = df['URL_FB_profile_x'].fillna(df['URL_FB_profile_y'])
# df['URL_IG'] = df['URL_IG_x'].fillna(df['URL_IG_y'])

# df['order'] = df['order'].fillna(0).astype(int)
# df_final = df[elecciones.columns]

# # df[''] = df['']
# # df[''] = df['']
# # df[''] = df['']

# df_final.to_csv("avergas.csv", index=False)


###############################################
# Diputados Córdoba
###############################################

# raw = pd.read_csv('data/dip_cordoba.csv')
# pipol = raw.rename(columns={'full_name': 'entity'})

# data_duckduckgo = harvester.collect_from_duckduckgo(pipol, 'cordoba')

# df = pd.merge(pipol, data_duckduckgo, on="entity", how="left")

# harvester.download(df, 'outputs/dip_cordoba')

###############################################
# Diputados Buenos Aires
###############################################

# raw = pd.read_csv('data/dip_bs_as.csv')
# pipol = raw.rename(columns={'full_name': 'entity'})

# data_duckduckgo = harvester.collect_from_duckduckgo(pipol, 'buenos aires')

# df = pd.merge(pipol, data_duckduckgo, on="entity", how="left")

# harvester.download(df, 'outputs/dip_bs_as')

###############################################
# Senadores Buenos Aires
###############################################

# raw = pd.read_csv('data/sen_bs_as.csv')
# pipol = raw.rename(columns={'full_name': 'entity'})

# data_duckduckgo = harvester.collect_from_duckduckgo(pipol, 'buenos aires')

# df = pd.merge(pipol, data_duckduckgo, on="entity", how="left")

# harvester.download(df, 'outputs/sen_bs_as')


# ###############################################
# # Merge 2023-07-10
# ###############################################

# import pandas as pd
# import numpy as np
# # Lectura de los csv
# captura = pd.read_csv("data/2023-07-10/captura.csv")
# cne = pd.read_csv("data/2023-07-10/cne.csv")
# # Union de las cargas de los voluntaries
# rejunte = pd.read_csv("data/2023-07-10/rejunte.csv")

# # Renombramos columna DNI a dni
# cne = cne.rename(columns={'DNI': 'dni'})

# # Quitamos Parlasur y suplentes
# cne = cne[cne['Cargo'] != 'PARLAMENTARIOS DEL MERCOSUR'] 
# cne = cne[cne['Subcategoria Cargo'] != 'SUPLENTES']
# cne['dni'] = cne['dni'].astype(int)
# rejunte['dni'] = rejunte['dni'].astype(int)
# rejunte = rejunte.drop_duplicates(['dni'])

# # Mergeo la CNE con carga de voluntaries
# df = pd.merge(cne, rejunte, how="left", on="dni")

# # Llename first_name con lo que haya en first_name
# df['first_name'] = df['first_name'].fillna(df['Nombres'])
# df['last_name'] = df['last_name'].fillna(df['Apellido'])
# df['full_name'] = df['full_name'].fillna(df['Precandidatura'])
# df['partido'] = df['AP']
# df['ballot_name'] = df['Nombre_lista'].fillna(df['ballot_name'])
# df['order'] = df['Posicion'].fillna(df['order'])
# df['state'] = df['Distrito'].fillna(df['state'])
# df['date_birth'] = df['Fecha Nacimiento'].fillna(df['date_birth'])
# df['gender'] = df['Genero'].fillna(df['gender'])
# df['Website'] = df['WEB'].fillna(df['Website'])
# df['URL_TW'] = df['Twitter'].fillna(df['URL_TW'])
# df['URL_IG'] = df['Instagram'].fillna(df['URL_IG'])
# df['URL_FB_page'] = df['Facebook'].fillna(df['URL_FB_page'])

# # Llenamos membership_type dead_or_alive
# df['membership_type'], df['dead_or_alive'] = 'campaigning_politician', 'alive'

# # Llenamos start_date y end_date
# df['start_date'], df['end_date'] = pd.to_datetime("2023-06-24"), pd.to_datetime("2023-08-13")

# # Llenamos is_substitute, is_titular
# df['is_substitute'], df['is_titular'] = "No", "Yes"

# # Llenamos role_type
# df['role_type'] = np.where(df['Cargo'] == 'PRESIDENTE Y VICEPRESIDENTE', np.nan, df['Cargo'])
# df['role_type'] = df['role_type'].fillna(df['Subcategoria Cargo']).replace({
#     'DIPUTADOS NACIONALES': 'legislatorLowerBody',
#     'SENADORES NACIONALES': 'legislatorUpperBody',
#     'VICEPRESIDENTE': 'VicePresident',
#     'PRESIDENTE': 'President',
# })


# # Dropeo de columnas
# columnas_finales = [x for x in list(captura.columns) if x not in ['has_descendants', 'previous_pubic_roles', 'Comentarios ']]
# final = df[columnas_finales]


# final.to_csv('data/2023-07-10/output.csv')



# ###############################################
# # Merge 2023-07-11
# ###############################################

# import pandas as pd
# import numpy as np

# # Lectura de los csv
# cne = pd.read_csv("data/2023-07-10/cne.csv")
# captura = pd.read_csv("data/2023-07-10/captura.csv")
# dl = pd.read_csv("data/2023-07-10/dl.csv")
# dl = dl.drop_duplicates(['dni'])
# rejunte = pd.read_csv("data/2023-07-10/rejunte.csv")
# rejunte['dni'] = rejunte['dni'].astype(int)
# rejunte = rejunte.drop_duplicates(['dni'])
# rejunte = rejunte[list(captura.columns)]


# def join_and_merge(df1, df2):
#     dnis_rejuntes = df1['dni'].unique()

#     #Agregamos dni faltante en rejunte
#     df2_sin_dni_df1 = df2[~df2['dni'].isin(dnis_rejuntes)]
#     df_completo = pd.concat([df1, df2_sin_dni_df1])

#     #Mergeamos con información nueva
#     df2_con_dni_df1= df2[df2['dni'].isin(dnis_rejuntes)]

#     columnas = {x: f"{x}_df2" for x in list(df2_con_dni_df1.columns) if x != "dni"} 

#     df2_con_dni_df1 = df2_con_dni_df1.rename(columns=columnas)   

#     df = pd.merge(df_completo, df2_con_dni_df1, on="dni", how="left")

#     for col in df1.columns:
#         if col != "dni":
#             df[col] = df[col].fillna(df[f"{col}_df2"])

#     df = df[df1.columns]
#     return df


# df = join_and_merge(rejunte, dl)



# # Renombramos columna DNI a dni, quitamos Parlasur y suplentes
# cne = cne.rename(columns={'DNI': 'dni'})
# cne['dni'] = cne['dni'].astype(int)
# cne = cne[cne['Cargo'] != 'PARLAMENTARIOS DEL MERCOSUR'] 
# cne = cne[cne['Subcategoria Cargo'] != 'SUPLENTES']

# # Mergeo la CNE con carga de voluntaries
# df = pd.merge(cne, df, how="outer", on="dni")

# # Llename first_name con lo que haya en first_name
# df['first_name'] = df['first_name'].fillna(df['Nombres'])
# df['last_name'] = df['last_name'].fillna(df['Apellido'])
# df['full_name'] = df['full_name'].fillna(df['Precandidatura'])
# df['partido'] = df['AP']
# df['ballot_name'] = df['ballot_name'].fillna(df['Nombre_lista'])
# df['order'] = df['order'].fillna(df['Posicion']).astype(int)
# df['state'] = df['state'].fillna(df['Distrito'])
# df['date_birth'] = df['date_birth'].fillna(df['Fecha Nacimiento'])
# df['gender'] = df['gender'].fillna(df['Genero'])
# df['Website'] = df['Website'].fillna(df['WEB'])
# df['URL_TW'] = df['URL_TW'].fillna(df['Twitter'])
# df['URL_IG'] = df['URL_IG'].fillna(df['Instagram'])
# df['URL_FB_page'] = df['URL_FB_page'].fillna(df['Facebook'])

# # Llenamos membership_type dead_or_alive
# df['membership_type'], df['dead_or_alive'] = 'campaigning_politician', 'alive'

# # Llenamos start_date y end_date
# df['start_date'], df['end_date'] = pd.to_datetime("2023-06-24"), pd.to_datetime("2023-08-13")

# # Llenamos is_substitute, is_titular
# df['is_substitute'], df['is_titular'] = "No", "Yes"

# # Llenamos role_type
# df['role_type'] = np.where(df['Cargo'] == 'PRESIDENTE Y VICEPRESIDENTE', np.nan, df['Cargo'])
# df['role_type'] = df['role_type'].fillna(df['Subcategoria Cargo']).replace({
#     'DIPUTADOS NACIONALES': 'legislatorLowerBody',
#     'SENADORES NACIONALES': 'legislatorUpperBody',
#     'VICEPRESIDENTE': 'VicePresident',
#     'PRESIDENTE': 'President',
# })


# # Dropeo de columnas
# final = df[list(captura.columns)]
# df['person_id'] = range(len(df))
# final.to_csv('data/2023-07-10/output.csv', index=False)
